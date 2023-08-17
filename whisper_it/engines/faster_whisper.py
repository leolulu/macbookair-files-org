from faster_whisper import WhisperModel


class FasterWhisper:
    def __init__(self, model_size="large-v2") -> None:
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16")

    def transcribe(self, media_path, word_timestamps=False):
        segments, info = self.model.transcribe(media_path, beam_size=5, word_timestamps=word_timestamps)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        return segments, info

if __name__ == "__main__":
    w = FasterWhisper()
    segments, info = w.transcribe("test.mp3")
    