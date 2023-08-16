import os
from typing import Optional
import whisper
from whisper.utils import WriteSRT
from moviepy.editor import VideoFileClip
from collections import defaultdict
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from whisper_it.utils.writer_util import write_srt


class OpenAIWhisper:
    def __init__(self, model_name="large") -> None:
        self.model = whisper.load_model(model_name)

    def transcribe(
        self,
        media_path,
        verbose: Optional[bool] = False,
        language: Optional[str] = None,
        write_txt: bool = True,
    ):
        media_path = os.path.abspath(media_path)
        media_path_without_ext = os.path.splitext(media_path)[0]
        result = self.model.transcribe(media_path, verbose=verbose, language=language)
        write_srt(result, media_path)
        if write_txt:
            with open(media_path_without_ext + ".txt", "a", encoding="utf-8") as f:
                for segment in result["segments"]:
                    f.write(segment["text"].strip() + "\n")  # type: ignore
        return result

    def detect_language(self, media_path):
        media_path = os.path.abspath(media_path)
        audio = whisper.load_audio(media_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        real_probs = probs[0] if isinstance(probs, list) else probs
        return max(probs, key=real_probs.get)  # type: ignore

    def detect_language_by_longer_material(self, media_path):
        lang_results = defaultdict(int)
        with VideoFileClip(media_path) as clip:
            duration = clip.duration
        start_time = 0
        while start_time < duration:
            end_time = min(clip.duration, start_time + 30)
            sub_media_file_path = f"_{start_time}_{end_time}".join(os.path.splitext(media_path))
            ffmpeg_extract_subclip(media_path, start_time, end_time, targetname=sub_media_file_path)
            lang_result = self.detect_language(sub_media_file_path)
            lang_results[lang_result] += 1
            print(f"语言检测结果：{lang_result}，时间：{start_time} - {end_time}")
            print(f"当前所有结果：{lang_results}")
            start_time += 30
            os.remove(sub_media_file_path)

        lang_results.pop("nn", None)
        return lang_results
