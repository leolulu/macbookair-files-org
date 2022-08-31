import os
import shutil
import subprocess
import sys

from utils.read_srt import read_srt


def concat_video(folder_path):
    os.chdir(folder_path)
    print(f"工作目录：{os.getcwd()}")

    if os.path.exists('filelist.txt'):
        os.remove('filelist.txt')
    with open('filelist.txt', 'a', encoding='utf-8') as f:
        for i in os.listdir('.'):
            if i == 'filelist.txt':
                continue
            print(f"Add: {i}")
            f.write(f"file '{i}'\n")
    file_name = f"{os.path.basename(folder_path)}_cut_dense.mp4"
    command = f'ffmpeg -f concat -safe 0 -i filelist.txt -c copy -y "{file_name}"'
    print(f"指令：{command}\n")
    subprocess.call(command, shell=True)
    shutil.move(file_name, os.path.dirname(folder_path))


def cut_video(video_path, srt_path):
    video_path = os.path.abspath(video_path)
    video_name = os.path.basename(video_path)
    output_dir = os.path.join(os.path.dirname(video_path), os.path.splitext(video_name)[0]+'_concat')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if srt_path is None:
        srt_path = os.path.splitext(video_path)[0] + '.srt'
    srt_datas = read_srt(srt_path)
    for idx, srt_data in enumerate(srt_datas):
        start_time, end_time, content = srt_data
        output_video_path = os.path.join(
            output_dir,
            "".join([
                os.path.splitext(video_name)[0],
                f"_{str(idx).zfill(6)}",
                os.path.splitext(video_name)[1]
            ])
        )
        command = f'ffmpeg -y -ss {start_time} -to {end_time} -i "{video_path}" -preset veryfast "{output_video_path}"'
        print(command)
        subprocess.call(command, shell=True)
    return output_dir


def run(video_path, srt_path=None):
    output_dir = cut_video(video_path, srt_path)
    concat_video(output_dir)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])

    # output_dir = cut_video(
    #     r"C:\fuck\新建文件夹\自慰初体验（直播）.mp4",
    #     r"C:\fuck\新建文件夹\自慰初体验（直播） (1).srt"
    # )
    # concat_video(r"C:\fuck\新建文件夹\自慰初体验（直播）_concat")
