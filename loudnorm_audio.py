import os
import sys
import subprocess


def cut_video(video_path):
    loudnormed_file_name = '_loudnormed'.join(os.path.splitext(video_path))
    exe_string = 'ffmpeg -i "{}" -af "loudnorm=I=-14:LRA=11:TP=-1.5, highpass=f=200, lowpass=f=3000" -c:v copy "{}"'
    exe_string = exe_string.format(video_path, loudnormed_file_name)
    print(exe_string)
    subprocess.call(exe_string, shell=True)


if __name__ == "__main__":
    video_path = sys.argv[1]
    cut_video(os.path.abspath(video_path))
