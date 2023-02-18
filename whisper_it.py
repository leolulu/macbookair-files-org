import os
from sys import meta_path
import whisper
from whisper.utils import WriteSRT


class WhisperIt:
    def __init__(self, model_name="large") -> None:
        self.model = whisper.load_model(model_name)

    def transcribe(self, media_path, verbose=False):
        media_path = os.path.abspath(media_path)
        media_path_without_ext = os.path.splitext(media_path)[0]
        result = self.model.transcribe(media_path, verbose=verbose)
        output_dir = os.path.dirname(media_path)
        writer = WriteSRT(output_dir)
        writer(result, media_path_without_ext)
        with open(media_path_without_ext+'.txt', 'w', encoding='utf-8') as f:
            f.write(str(result['text']))

    def close(self):
        del self.model
