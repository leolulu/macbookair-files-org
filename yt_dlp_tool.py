from pathlib import Path
import subprocess
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dl_dir', help='视频文件目录的路径，必须使用绝对路径，默认为当前用户的"下载"文件夹', default=str(Path.home() / "Downloads"))
parser.add_argument('--mp4', help='是否需要【启用】后处理【转码】为mp4，默认不启用，如果开启，会禁用封装', action='store_true')
parser.add_argument('--unremux', help='是否需要【禁用】后处理【封装】为mp4，默认开启封装', action='store_true')
parser.add_argument('-d', '--dry_run', help='是否启动dry run模式', action='store_true')
parser.add_argument('url', help='youtube视频url')
args = parser.parse_args()

download_command_template = 'yt-dlp --ignore-errors --windows-filenames --proxy socks5://127.0.0.1:10808 --mark-watched --retries 99 --file-access-retries 99 --fragment-retries 99 -o "{temp_folder}/%(title)s.%(ext)s" #encode-video-placeholder# #remux-video-placeholder# {simulate} --cookies-from-browser chrome "{url}"'
download_command_template = download_command_template.format(url=args.url, temp_folder=args.dl_dir.replace('\\', '/').replace('\\\\', '/'), simulate="-s" if args.dry_run else "")


if args.unremux:
    download_command = (
        download_command_template
        .replace('#remux-video-placeholder#', '')
        .replace('#encode-video-placeholder#', (
            '--recode-video mp4 --add-metadata --postprocessor-args "-movflags faststart"' if args.mp4 else ''
        ))
    )
else:
    download_command = download_command_template.replace('#remux-video-placeholder#', '--remux-video "mp4"').replace('#encode-video-placeholder#', '')


print(f"下载指令：{download_command}")
subprocess.Popen(download_command, shell=True)
