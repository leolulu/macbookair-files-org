import argparse
import os
import shutil
import subprocess
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def yt_dlp():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dl_dir', help='视频文件目录的路径，必须使用绝对路径，默认为当前用户的"下载"文件夹', default=str(Path.home() / "Downloads"))
    parser.add_argument('--mp4', help='是否需要【启用】后处理【转码】为mp4，默认不启用，如果开启，会禁用封装', action='store_true')
    parser.add_argument('--unremux', help='是否需要【禁用】后处理【封装】为mp4，默认开启封装', action='store_true')
    parser.add_argument('--postprefix', help='是否需要增加文件名后缀')
    parser.add_argument('--temp_folder_name', help='指定一个临时文件夹的名称，默认会随机生成', default=str(int(time.time())))
    parser.add_argument('url', help='youtube视频url')
    args = parser.parse_args()

    temp_folder = args.temp_folder_name
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    download_command_template = 'yt-dlp --ignore-errors --windows-filenames --proxy socks5://127.0.0.1:10808 --mark-watched --retries 99 --file-access-retries 99 --fragment-retries 99 -o "{temp_folder}/%(title)s.%(ext)s" #encode-video-placeholder# #remux-video-placeholder# --cookies-from-browser chrome "{url}"'
    download_command_template = download_command_template.format(url=args.url, temp_folder=temp_folder)

    if args.unremux:
        download_command = (
            download_command_template
            .replace('#remux-video-placeholder#', '')
            .replace('#encode-video-placeholder#', (
                '--rencode-video mp4 --add-metadata --postprocessor-args "-movflags faststart"' if args.mp4 else ''
            ))
        )
    else:
        download_command = download_command_template.replace('#remux-video-placeholder#', '--remux-video "mp4"').replace('#encode-video-placeholder#', '')

    try:
        print(f"下载指令：{download_command}")
        subprocess.call(download_command, shell=True)

        for f_name in os.listdir(temp_folder):
            f_path = os.path.join(temp_folder, f_name)
            if args.postprefix:
                f_path_with_postprefix = args.postprefix.join(os.path.splitext(f_path))
                os.rename(f_path, f_path_with_postprefix)
                shutil.move(f_path_with_postprefix, args.dl_dir)
            else:
                shutil.move(f_path, args.dl_dir)
    except:
        traceback.print_exc()
    finally:
        shutil.rmtree(temp_folder)


if __name__ == "__main__":
    yt_dlp()
