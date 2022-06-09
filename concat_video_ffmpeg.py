import os
import re
import subprocess
import sys


def concat_video(folder_path):
    os.chdir(folder_path)
    print(os.getcwd())
    if os.path.exists('filelist.txt'):
        os.remove('filelist.txt')
    with open('filelist.txt', 'a', encoding='utf-8') as f:
        for i in os.listdir('.'):
            if i == 'filelist.txt':
                continue
            f.write(f"file '{i}'\n")
    folder_path = os.path.basename(folder_path)
    command = f'ffmpeg -f concat -safe 0 -i filelist.txt -c copy -an -y {folder_path}.mp4'
    print(command)
    subprocess.call(command, shell=True)


def specify_run():
    for i in sys.argv[1:]:
        concat_video(i)


def unspecify_run():
    for i in [d for d in os.listdir('.') if os.path.isdir(d)]:
        concat_video(i)


def parent_run():
    for i in [d for d in os.listdir('.') if os.path.isdir(d)]:
        if re.match(r"^202", i):
            os.chdir(i)
            unspecify_run()
            os.chdir('..')
        else:
            unspecify_run()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        specify_run()
    else:
        parent_run()
