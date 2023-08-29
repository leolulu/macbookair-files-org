import io
import json
import os
import re
import subprocess
import time
from threading import Thread
from typing import Iterable, List

import torch
import zhconv
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from tqdm import tqdm


class FasterWhisper:
    def __init__(self, model_size="large-v2", local_files_only=True) -> None:
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16", local_files_only=local_files_only)
        self.pyannote_pipeline = None

    def transcribe(self, media_path, word_timestamps=True, language=None):
        segments, info = self.model.transcribe(media_path, beam_size=5, word_timestamps=word_timestamps, language=language)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        segments_result: List[Segment] = []
        total_duration = int(info.duration)

        td_len = str(len(str(total_duration)))
        last_burst = 0.0
        set_delay = 0.1
        global timestamp_prev, timestamp_last
        timestamp_prev = 0  # last timestamp in previous chunk
        timestamp_last = 0
        capture = io.StringIO()

        def pbar_delayed():  # to get last timestamp from chunk
            global timestamp_prev
            time.sleep(set_delay)  # wait for whole chunk to be iterated
            pbar.update(timestamp_last - timestamp_prev)
            timestamp_prev = timestamp_last
            print(capture.getvalue().splitlines()[-1])

        with tqdm(
            file=capture,
            total=total_duration,
            unit=" seconds",
            smoothing=0.00001,
            bar_format="{percentage:3.0f}% | {n_fmt:>" + td_len + "}/{total_fmt} | {elapsed}<<{remaining} | {rate_noinv_fmt}",
        ) as pbar:
            for segment in segments:
                if info.language == "zh":
                    segment = segment._replace(text=zhconv.convert(segment.text, "zh-cn"))
                timestamp_last = round(segment.end)
                time_now = time.time()
                if time_now - last_burst > set_delay:  # catch new chunk
                    last_burst = time_now
                    Thread(target=pbar_delayed, daemon=False).start()
                segments_result.append(segment)
            time.sleep(set_delay + 0.3)
            if timestamp_last < total_duration:
                pbar.update(total_duration - timestamp_last)
                print(capture.getvalue().splitlines()[-1])

        return segments_result, info

    def transcribe_to_file(
        self,
        media_path,
        word_timestamps=True,
        language=None,
        with_txt=False,
        with_json=False,
        with_diarization=False,
    ):
        video_duration = self.get_video_duration(media_path)
        print(f"视频时长为: {video_duration}")
        b_time = time.time()
        segments, info = self.transcribe(media_path, word_timestamps=word_timestamps, language=language)
        print(f"音转文环节运行时间为：{int(time.time()-b_time)}秒，速率为：{round(video_duration/(time.time()-b_time),2)}")
        srt_content = self.generate_srt(self.segments_to_srt_subtitles(segments))
        with open(os.path.splitext(media_path)[0] + ".srt", "w", encoding="utf-8") as f:
            f.write(srt_content)
        if with_txt:
            with open(os.path.splitext(media_path)[0] + ".txt", "w", encoding="utf-8") as f:
                f.write("\n".join([i.text for i in segments]))
        if with_diarization:
            b_time = time.time()
            diarization_info = self.get_diarization(media_path)
            print(f"说话人识别环节运行时间为：{int(time.time()-b_time)}秒，速率为：{round(video_duration/(time.time()-b_time),2)}")
        if word_timestamps and with_json:
            json_data = {
                "asr_info": [
                    {
                        "start": s.start,
                        "end": s.end,
                        "text": s.text,
                        "words": [{"start": w.start, "end": w.end, "word": w.word} for w in s.words],  # type:ignore
                    }
                    for s in segments
                ],
            }
            if with_diarization:
                json_data["diarization_info"] = [{"start": d[0], "end": d[1], "label": d[2]} for d in diarization_info]  # type: ignore
            with open(os.path.splitext(media_path)[0] + ".json", "w", encoding="utf-8") as f:
                f.write(json.dumps(json_data, indent=2, ensure_ascii=False))

    def generate_srt(self, subtitles):
        def convert_to_srt_time_format(original_seconds):
            hours = int(original_seconds // 3600)
            minutes = int((original_seconds % 3600) // 60)
            seconds = int(original_seconds % 60)
            milliseconds = int((original_seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

        srt_content = ""
        counter = 1
        for subtitle in subtitles:
            start_time, end_time, text = subtitle
            srt_content += f"{counter}\n"
            srt_content += f"{convert_to_srt_time_format(start_time)} --> {convert_to_srt_time_format(end_time)}\n"
            srt_content += f"{text}\n\n"
            counter += 1
        return srt_content

    def segments_to_srt_subtitles(self, segments: Iterable[Segment]):
        return [(i.start, i.end, i.text) for i in segments]

    def get_diarization(self, media_path):
        png_path = os.path.splitext(media_path)[0] + ".png"
        audio_path = self.media_to_mp3(media_path)
        if not self.pyannote_pipeline:
            self.pyannote_pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization", use_auth_token="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"
            ).to(torch.device("cuda"))
        with ProgressHook() as hook:
            diarization = self.pyannote_pipeline(audio_path, hook=hook)
        png_data = diarization._repr_png_()
        with open(png_path, "wb") as f:
            f.write(png_data)
        os.remove(audio_path)
        return [(i[0].start, i[0].end, i[2]) for i in diarization.itertracks(yield_label=True)]

    def get_video_duration(self, video_path):
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8")
        match = re.search(r"(\d+(?:\.\d+)?)", output)
        if match:
            return float(match.group(1))
        else:
            raise UserWarning(f"无法正确获取视频时长:\n{output}")

    def media_to_mp3(self, video_path):
        mp3_path = os.path.splitext(video_path)[0] + ".mp3"
        cmd = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", mp3_path]
        subprocess.run(cmd)
        return mp3_path


if __name__ == "__main__":
    w = FasterWhisper(local_files_only=True)
    w.transcribe_to_file(
        r"C:\Users\sisplayer\Downloads\09e93919b4bad41ce70d2f2ff949043d.mp4",
        with_json=True,
        with_txt=True,
        with_diarization=True,
    )
