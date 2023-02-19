import argparse
import os
import shutil
import traceback
from dataclasses import dataclass
from multiprocessing import Process, Queue
from typing import Optional

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


@dataclass(frozen=True)
class WhisperTask:
    media_path: str
    verbose: Optional[bool] = False


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
                w.transcribe(task.media_path, task.verbose)
                print("任务处理完成...")
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('media_path', help='音视频文件的路径')
    parser.add_argument('-v', '--verbose', help='是否需要详细输出处理过程', action='store_true')
    args = parser.parse_args()
    w = WhisperIt()
    w.transcribe(args.media_path, verbose=args.verbose)
