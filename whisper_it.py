import argparse
import os
import shutil
import traceback
from dataclasses import dataclass, field
from multiprocessing import Process, Queue
from typing import Callable, List, Optional

import dill
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
        return result

    def detect_language(self, media_path):
        media_path = os.path.abspath(media_path)
        audio = whisper.load_audio(media_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        real_probs = probs[0] if isinstance(probs, list) else probs
        return max(probs, key=real_probs.get)  # type: ignore


@dataclass(frozen=False)
class WhisperTask:
    media_path: str
    verbose: Optional[bool] = False
    target_languages: Optional[List[str]] = None
    post_func: Optional[Callable] = None
    post_func_bytes: Optional[bytes] = field(init=False)

    def __post_init__(self):
        if self.post_func:
            self.post_func_bytes = dill.dumps(self.post_func)
        else:
            self.post_func_bytes = None
        del self.post_func


class WhisperTaskHandler:
    def __init__(self) -> None:
        self.queue = Queue()
        self._launch_worker_process()

    def _launch_worker_func(self):
        print("开始加载模型...")
        w = WhisperIt()
        print("模型加载完毕，等待接收任务...")
        while True:
            task = self.queue.get()
            print(f"开始处理任务：{task}")
            try:
                if task.target_languages:
                    language = w.detect_language(task.media_path)
                    if language not in task.target_languages:
                        print(f"检测出语言为[{language}]，不在目标语言[{task.target_languages}]中，跳过处理...")
                        language_folder = os.path.join(os.path.dirname(task.media_path), language)
                        if not os.path.exists(language_folder):
                            os.mkdir(language_folder)
                        shutil.move(task.media_path, language_folder)
                        continue
                result = w.transcribe(task.media_path, task.verbose)
                print("任务处理完成...")
                if task.post_func_bytes:
                    post_func = dill.loads(task.post_func_bytes)
                    post_func(task.media_path, result)
            except:
                print("处理任务失败，跳过...")
                traceback.print_exc()
                self._handle_error_file(task.media_path)

    def _handle_error_file(self, file_path):
        error_folder = os.path.join(os.path.dirname(file_path), 'error_files')
        if not os.path.exists(error_folder):
            os.mkdir(error_folder)
        shutil.move(file_path, error_folder)

    def _launch_worker_process(self):
        self.whisper_process = Process(target=self._launch_worker_func)
        self.whisper_process.start()

    def add_task(self, task: WhisperTask):
        print(f"添加任务：{os.path.basename(task.media_path)}")
        if str(task.media_path).lower().split(".")[-1] in ['txt', 'srt']:
            print("  文件格式不合法，跳过!")
            return
        self.queue.put(task)

    def close(self):
        self.whisper_process.terminate()
        self.whisper_process.close()
        print("模型已关闭！")


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument('media_path', help='音视频文件的路径')
    # parser.add_argument('-v', '--verbose', help='是否需要详细输出处理过程', action='store_true')
    # args = parser.parse_args()
    # w = WhisperIt()
    # w.transcribe(args.media_path, verbose=args.verbose)
    def post_func(media_path, result):
        import os
        import shutil
        srt_path = os.path.splitext(media_path)[0] + '.srt'
        txt_path = os.path.splitext(media_path)[0] + '.txt'
        if os.path.getsize(txt_path) < 128:
            bad_result_folder = os.path.join(os.path.dirname(media_path), 'bad_results')
            if not os.path.exists(bad_result_folder):
                os.mkdir(bad_result_folder)
            for i in [media_path, srt_path, txt_path]:
                shutil.move(i, bad_result_folder)

    wth = WhisperTaskHandler()
    _dir = r"C:\Users\sisplayer\Downloads\BNWO content"
    for i in os.listdir(_dir):
        i = os.path.join(_dir, i)
        wth.add_task(WhisperTask(i, True, ['en'], post_func))
