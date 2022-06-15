import os
import re
import subprocess
import sys
from typing import overload


def concat_video(folder_path, *keywords):
    os.chdir(folder_path)
    print(f"工作目录：{os.getcwd()}")
    if len(keywords) == 0:
        keywords = [None]
    for keyword in keywords:
        print(f"当前keyword：{keyword}")
        if os.path.exists('filelist.txt'):
            os.remove('filelist.txt')
        with open('filelist.txt', 'a', encoding='utf-8') as f:
            for i in os.listdir('.'):
                if i == 'filelist.txt':
                    continue
                if (keyword != None) and (not re.search(r".*?" + keyword.strip() + r".*?", i)):
                    continue
                print(f"Add: {i}")
                f.write(f"file '{i}'\n")
        file_name = f"{os.path.basename(folder_path)}_{keyword}" if keyword != None else os.path.basename(folder_path)
        command = f'ffmpeg -f concat -safe 0 -i filelist.txt -c copy -y "{file_name}.mp4"'
        print(f"指令：{command}\n")
        subprocess.call(command, shell=True)


# def specify_run(folder_path, *keywords):
#     concat_video(folder_path, keywords)


# def unspecify_run():
#     for i in [d for d in os.listdir('.') if os.path.isdir(d)]:
#         concat_video(i)


# def parent_run():
#     for i in [d for d in os.listdir('.') if os.path.isdir(d)]:
#         if re.match(r"^202", i):
#             os.chdir(i)
#             unspecify_run()
#             os.chdir('..')
#         else:
#             unspecify_run()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        concat_video(sys.argv[1])
    elif len(sys.argv) >= 3:
        concat_video(sys.argv[1], *sys.argv[2:])
