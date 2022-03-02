# https://www.luyinzhushou.com/voice2text/

from posixpath import commonpath
import subprocess
import os
import sys
import re
import shutil


LIMIT = 20 * 1024 * 1024


def get_length(file_path):
    command = f'ffprobe "{file_path}"'
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = s.communicate()
    result = re.findall(r"Duration: (\d+):(\d+):([\d\.]+),", stderr)[0]
    hour = result[0]
    minute = result[1]
    second = result[2]
    duration = int(hour) * 3600 + int(minute) * 60 + int(float(second))
    return duration


def get_bitrate(duration):
    return round(LIMIT / duration * 8 / 1000)


def process_fix_length(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    interval = 4175
    btime = 0
    empyt_string = "Output file is empty"
    output_path = os.path.dirname(file_path)
    serial_no = 0

    while True:
        serial_no += 1
        output_name = os.path.join(output_path, file_name + "-" + str(serial_no))

        command_mp3 = f'ffmpeg -i "{file_path}" -ss {btime} -t {interval} -ab 44k -y {output_name}.mp3'
        command_mp4 = f'ffmpeg -i "{file_path}" -ss {btime} -t {interval} -c copy -y {output_name}.mp4'

        s = subprocess.Popen(command_mp3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = s.communicate()
        if empyt_string in stdout or empyt_string in stderr:
            os.remove(f"{output_name}.mp3")
            break

        subprocess.call(command_mp4, shell=True)

        btime += interval


def process_baseon_bitrate_only_audio(file_path, bit_rate):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.dirname(file_path)
    output_name = os.path.join(output_path, file_name)
    output_finish_path = f"{output_name}.mp3"
    output_working_path = f"{output_name}_working.mp3"
    output_lasttime_path = f"{output_name}_lasttime.mp3"
    lasttime_bigger = False
    lasttime_smaller = False

    def convert():
        command_mp3 = f'ffmpeg -i "{file_path}"  -ab {bit_rate}k -y "{output_working_path}"'
        print(command_mp3)
        s = subprocess.Popen(command_mp3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = s.communicate()

    while True:
        convert()
        currrent_size_human = f"{round(os.path.getsize(output_working_path) / 1024 /1024,2)}MB"
        if os.path.getsize(output_working_path) > LIMIT:
            if lasttime_smaller == True:
                print(f"文件大足够了【{currrent_size_human}】，当前码率为：{bit_rate}")
                break
            print(f"文件大了【{currrent_size_human}】，减少码率，当前码率为：{bit_rate}")
            lasttime_bigger = True
            bit_rate -= 1
        elif os.path.getsize(output_working_path) < LIMIT:
            if lasttime_bigger == True:
                print(f"文件小足够了【{currrent_size_human}】，当前码率为：{bit_rate}")
                break
            print(f"文件小了【{currrent_size_human}】，增大码率，当前码率为：{bit_rate}")
            lasttime_smaller = True
            bit_rate += 1
        else:
            break
        shutil.copy(output_working_path, output_lasttime_path)

    if os.path.exists(output_lasttime_path):
        os.rename(output_lasttime_path, output_finish_path)
        os.remove(output_working_path)
    else:
        os.rename(output_working_path, output_finish_path)


if __name__ == "__main__":
    # file_path = os.path.abspath(sys.argv[1])
    file_path = r"C:\Users\sisplayer\Downloads\新建文件夹\all.mp4"
    duration = get_length(file_path)
    bitrate = get_bitrate(duration)
    # process_baseon_bitrate_only_audio(file_path, bitrate)
    process_fix_length(file_path)
