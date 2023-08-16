from engines.openai_whisper import OpenAIWhisper
from utils.dict_util import get_target_lang
import os


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument('media_path', help='音视频文件的路径')
    # parser.add_argument('-v', '--verbose', help='是否需要详细输出处理过程', action='store_true')
    # args = parser.parse_args()
    # w = WhisperIt()
    # w.transcribe(args.media_path, verbose=args.verbose)

    # def post_func(media_path, result):
    #     import os
    #     import shutil
    #     srt_path = os.path.splitext(media_path)[0] + '.srt'
    #     txt_path = os.path.splitext(media_path)[0] + '.txt'
    #     if os.path.getsize(txt_path) < 256:
    #         bad_result_folder = os.path.join(os.path.dirname(media_path), 'bad_results')
    #         if not os.path.exists(bad_result_folder):
    #             os.mkdir(bad_result_folder)
    #         for i in [media_path, srt_path, txt_path]:
    #             shutil.move(i, bad_result_folder)

    # wth = WhisperTaskHandler()
    # _dir = r"\\192.168.123.221\共享文件夹\gif2"
    # for current_dir, folders, files in os.walk(_dir):
    #     for i in files:
    #         i = os.path.join(current_dir, i)
    #         wth.add_task(WhisperTask(i, False, ['en'], post_func))
    w = OpenAIWhisper()
    media_paths = [r"C:\Users\sisplayer\Downloads\LES MILLS CORE TUTORIAL.mp4"]
    # folder_path = r"\\192.168.123.222\transfer\良叔《偷心聊法Plus》"
    # media_paths = [os.path.join(folder_path, i) for i in os.listdir(folder_path)]

    for media_path in media_paths:
        print(media_path)
        result = w.detect_language_by_longer_material(media_path)
        print(result)
        w.transcribe(media_path, language=get_target_lang(result), write_txt=False)
        # w.transcribe(media_path, write_txt=False, language="de")
