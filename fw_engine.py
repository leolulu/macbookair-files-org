from typing import Iterable
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
import os


class FasterWhisper:
    def __init__(self, model_size="large-v2", local_files_only=True) -> None:
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16", local_files_only=local_files_only)

    def transcribe(self, media_path, word_timestamps=False, language=None):
        segments, info = self.model.transcribe(media_path, beam_size=5, word_timestamps=word_timestamps, language=language)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        return list(segments), info

    def transcribe_to_srt(self, media_path, word_timestamps=False, language=None, with_txt=False):
        segments, info = self.transcribe(media_path, word_timestamps=word_timestamps, language=language)
        srt_content = self.generate_srt(self.segments_to_srt_subtitles(segments))
        with open(os.path.splitext(media_path)[0] + ".srt", "w", encoding="utf-8") as f:
            f.write(srt_content)
        if with_txt:
            with open(os.path.splitext(media_path)[0] + ".txt", "w", encoding="utf-8") as f:
                f.write("\n".join([i.text for i in segments]))

    def generate_srt(self, subtitles):
        def convert_to_srt_time_format(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            milliseconds = int((seconds % 1) * 1000)
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


if __name__ == "__main__":
    w = FasterWhisper(local_files_only=True)
    w.transcribe_to_srt(
        r"C:\Users\sisplayer\Downloads\CONFIDENCE BABY ! 💪💪.mp4",
        word_timestamps=False,
        with_txt=True,
    )
