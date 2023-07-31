from engines.whisper_it import WhisperIt


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
    w = WhisperIt()
    result = w.detect_language_by_longer_material(r"\\d3\qbit_download\sharing\202306044444\BEASTIALITY\Doggie rot girl.mp4")
    print(result)    
