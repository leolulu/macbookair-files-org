import argparse
import re
import subprocess
import os
import sys


def get_length(file_path):
    command = f'ffprobe "{file_path}"'
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = s.communicate()
    result = re.findall(r"Duration: (\d+):(\d+):([\d\.]+),", stderr)[0]
    hour = result[0]
    minute = result[1]
    second = result[2]
    duration = int(hour) * 3600 + int(minute) * 60 + float(second)
    return duration


def cut_video(file_path, interval: int, encode: bool):
    duration = get_length(file_path)
    btime = 0
    idx = 1

    while btime < duration:
        etime = min(btime + interval, duration)
        output_name = f"_{str(idx).zfill(3)}".join(os.path.splitext(file_path))
        exe_string = f'ffmpeg -ss {btime} -to {etime} -accurate_seek -i "{file_path}" {"" if encode else "-codec copy"} -map_chapters -1 -avoid_negative_ts 1 "{output_name}"'
        print(f"指令：{exe_string}")
        subprocess.run(exe_string, shell=True)
        btime += interval
        idx += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file_path", help="媒体路径")
    parser.add_argument("interval", help="每段切分的时长", type=int)
    parser.add_argument("-e", "--encode", help="是否需要重编码", action="store_true")
    args = parser.parse_args()
    cut_video(args.file_path, args.interval, args.encode)
