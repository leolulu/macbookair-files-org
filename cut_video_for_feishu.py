import os
import sys
import subprocess
import json
import traceback
import math


def timeFormatTransformer(time_num):
    '''
    毫秒转换成时分秒毫秒
    '''
    millisecond = str(time_num % 1000 / 1000).split('.')[-1].ljust(3, '0')
    hour = str(int(int(time_num / 1000) / 3600)).zfill(2)
    minute = str(int(int(time_num / 1000) % 3600 / 60)).zfill(2)
    second = str(int(time_num / 1000) % 3600 % 60).zfill(2)
    time_str = '{}:{}:{}.{}'.format(hour, minute, second, millisecond)
    return time_str


def getMp3Len(file_path):
    command = "ffprobe -loglevel quiet -print_format json -show_format -show_streams -i {}".format(file_path)
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    data = json.loads(temp)["format"]['duration']
    return float(data)


def getFileSizeByMB(file_path):
    return os.path.getsize(file_path)/1024/1024/1024


def getSegList(size, length):
    seq_list = []
    num = math.ceil(size/3.9)
    every_length = int(length/num)
    last_time = 0
    for _ in range(num-1):
        period_end_time = last_time+every_length
        seq_list.append([
            timeFormatTransformer((last_time)*1000),
            timeFormatTransformer((period_end_time)*1000)
        ])
        last_time = period_end_time
        length -= every_length
    seq_list.append([
        timeFormatTransformer((last_time)*1000),
        timeFormatTransformer((last_time+length)*1000)
    ])
    return seq_list


def cut_video(video_path, seq_list):
    for i, time_tuple in enumerate(seq_list, start=1):
        every_file_name = '-{}'.format(i).join(os.path.splitext(video_path))
        exe_string = 'ffmpeg -ss {} -to {} -accurate_seek -i "{}" -codec copy -map_chapters -1 -avoid_negative_ts 1 "{}"'
        exe_string = exe_string.format(time_tuple[0], time_tuple[1], video_path, every_file_name)
        print(exe_string)
        subprocess.call(exe_string, shell=True)


if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        file_path = os.path.abspath(file_path)
        size = getFileSizeByMB(file_path)
        length = getMp3Len(file_path)
        seq_list = getSegList(size, length)
        cut_video(file_path, seq_list)
