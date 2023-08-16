from faster_whisper import WhisperModel


class MyWhisperX:
    def __init__(self) -> None:
        self.model_size = WhisperModel("large-v2", device="cuda", compute_type="float16")

    def transcribe(self, media_path, beam_size=5, word_timestamps=False):
        segments, info = self.model_size.transcribe(media_path, beam_size=beam_size, word_timestamps=word_timestamps)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        return segments, info
