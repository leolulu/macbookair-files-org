import argparse
import math
import os
import re
import shutil
import subprocess
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from typing import Tuple

import cv2
import numpy as np
import requests
from tqdm import tqdm


def check_video_corrupted(video_file_path):
    command = f'ffprobe "{video_file_path}"'
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    except UnicodeDecodeError:
        result = subprocess.run(command, capture_output=True, text=True)
    is_corrupted, width, height = True, None, None
    for line_content in result.stderr.split("\n"):
        if "Stream" in line_content and "Video" in line_content:
            width, height = re.findall(r", (\d+)x(\d+)[ ,]", line_content)[0]
            is_corrupted = False
    return is_corrupted, width, height


def move_with_optional_security(source, target, backup_target=None, msg=""):
    try:
        shutil.move(source, target)
    except:
        if backup_target:
            shutil.move(source, target)
    print(msg)


def get_font_location(frame, content: str, fontFace: int, font_scale: float, thickness: int) -> Tuple[int, int]:
    (text_width, text_height), _ = cv2.getTextSize(content, fontFace, font_scale, thickness)
    start_x = min(0, frame.shape[1] - text_width)
    start_y = max(0, text_height + 10)
    return (start_x, start_y)


def gen_pic_thumbnail(video_path, frame_interval, rows, cols, height, width, start_offset=0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise UserWarning("无法打开视频文件!")
    thumbnails = []
    for i in tqdm(range(rows * cols)):
        # 定位到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
        ret, frame = cap.read()
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
        if ret:
            # 计算时间戳
            seconds_total = milliseconds / 1000 + start_offset
            hours = int(seconds_total // 3600)
            seconds_total %= 3600
            minutes = int(seconds_total // 60)
            seconds = int(seconds_total % 60)
            timestamp = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            # 在图像的右上角添加时间戳（包括轮廓）
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = frame.shape[0] / 1080 * 4
            inner_white = (font_scale, 12)
            outer_black = (font_scale, 6)
            cv2.putText(
                frame,
                timestamp,
                get_font_location(frame, timestamp, font_face, *inner_white),
                font_face,
                inner_white[0],
                (0, 0, 0),
                inner_white[1],
            )
            cv2.putText(
                frame,
                timestamp,
                get_font_location(frame, timestamp, font_face, *outer_black),
                font_face,
                outer_black[0],
                (255, 255, 255),
                outer_black[1],
            )
            thumbnails.append(frame)
        else:
            thumbnails.append(np.zeros((height, width, 3), dtype=np.uint8))
    cap.release()

    # 计算缩略图的大小
    thumbnail_width = width * cols
    thumbnail_height = height * rows

    # 创建一个空白的背景图像
    thumbnail = np.zeros((thumbnail_height, thumbnail_width, 3), dtype=np.uint8)

    # 将每个缩略图放置到背景图像上
    for i in range(rows):
        for j in range(cols):
            thumbnail[i * height : (i + 1) * height, j * width : (j + 1) * width, :] = thumbnails[i * cols + j]

    # 保存缩略图
    output_path_img = os.path.splitext(video_path)[0] + ".jpg"
    temp_output_path_img = os.path.join(str(Path.home() / "Downloads"), f"WIP_{uuid.uuid4().hex}.jpg")
    print(f"缩略图保存路径为：{output_path_img}")
    if os.path.exists(output_path_img):
        os.remove(output_path_img)
    cv2.imwrite(temp_output_path_img, thumbnail)

    threading.Thread(
        target=move_with_optional_security,
        args=(
            temp_output_path_img,
            output_path_img,
            os.path.join(os.path.dirname(temp_output_path_img), os.path.basename(output_path_img)),
            "图片缩略图移动到目标目录完毕...",
        ),
    ).start()


def gen_video_thumbnail(
    video_path, preset, height, fps, duration_in_seconds, frame_interval, rows, cols, max_thumb_duration, start_offset=0
):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path_video = os.path.splitext(video_path)[0] + ".tbnl"
    temp_output_path_video = os.path.join(str(Path.home() / "Downloads"), f"WIP_{uuid.uuid4().hex}.mp4")
    # 生成视频缩略图
    # 生成中间文件落盘
    key_timestamp = [i * frame_interval / fps for i in range(rows * cols)]
    thumbnail_duration = min(max_thumb_duration, math.ceil(duration_in_seconds / (rows * cols)))
    max_output_height = 2160
    input_template = ' -ss {start_time} -t {duration} -i "{input_file_path}" '
    footage_paths = []
    gen_footage_commands = []
    intermediate_file_paths = []
    for i in key_timestamp:
        gen_footage_command = "ffmpeg " + input_template.format(start_time=i, duration=thumbnail_duration, input_file_path=video_path)
        filter_commands = []
        if height > max_output_height / rows:
            target_height = int(max_output_height / rows)
            target_height = target_height if target_height % 2 == 0 else target_height - 1
            filter_commands.append(f"scale=w=-2:h={target_height}")
        filter_drawtext_command = r"drawtext=text='%{pts\:gmtime\:drawtext_pts_offset\:%H\\\:%M\\\:%S}':x=10:y=10:fontsize=h/10:fontcolor=white:bordercolor=black:borderw=2"
        filter_drawtext_command = filter_drawtext_command.replace("drawtext_pts_offset", str(int(i) + start_offset))
        filter_commands.append(filter_drawtext_command)
        gen_footage_command += f" -vf {','.join(filter_commands)} "
        output_file_path = os.path.join(
            str(Path.home() / "Downloads"),
            f"{video_name[:2]}-{video_name[-2:]}-{round(i,3)}-{str(time.time())[-3:]}.mp4",
        )
        footage_paths.append(output_file_path)
        gen_footage_command += f" -preset {preset} -y "
        gen_footage_command += f'"{output_file_path}"'
        intermediate_file_paths.append(output_file_path)
        gen_footage_commands.append(gen_footage_command)
    with ThreadPoolExecutor(os.cpu_count()) as exe:
        exe.map(lambda c: subprocess.run(c, shell=True), gen_footage_commands)

    # 检查中间文件是否损坏
    print("开始检查中间文件是否损坏...")
    corrupted_file_paths = []
    intermediate_file_dimension: Tuple[int, int] = None  # type: ignore
    for intermediate_file_path in intermediate_file_paths:
        is_corrupted, intermediate_file_width, intermediate_file_height = check_video_corrupted(intermediate_file_path)
        if is_corrupted:
            corrupted_file_paths.append(intermediate_file_path)
        else:
            if intermediate_file_dimension is None:
                intermediate_file_dimension = (intermediate_file_width, intermediate_file_height)  # type: ignore
    # 修复受损的中间文件
    if corrupted_file_paths:
        print(f"开始修复以下受损文件:")
        print("\n".join(corrupted_file_paths))
        for corrupted_file_path in corrupted_file_paths:
            fix_command = 'ffmpeg -f lavfi -i color=c=gray:s={}x{}:d=1 -r {} -c:v libx264 -y "{}"'.format(
                intermediate_file_dimension[0], intermediate_file_dimension[1], fps, corrupted_file_path
            )
            print(f"修复指令：{fix_command}")
            subprocess.run(fix_command, shell=True)

    # 合并中间文件
    command = "ffmpeg "
    for footage_path in footage_paths:
        command += f' -i "{footage_path}" '
    # 生成filter_complex指令
    filter_complex_template = ' -filter_complex "{filter_complex_section}" '
    h_commands = []
    row_ids = []
    for r_num in range(rows):
        h_command = "".join([f"[{r_num*cols+i}:v]" for i in range(cols)])
        h_command += f"hstack=inputs={cols}[row{r_num}]"
        row_ids.append(f"[row{r_num}]")
        h_commands.append(h_command)
    h_commands = ";".join(h_commands)
    v_commands = "".join([i for i in row_ids])
    if len(row_ids) > 1:
        v_commands += f"vstack=inputs={rows}[out_final]"
    else:
        v_commands += f"null[out_final]"
    filter_complex_command = filter_complex_template.format(filter_complex_section=";".join([h_commands, v_commands]))
    command += filter_complex_command
    # 其他指令部分
    command += f' -map "[out_final]" -preset {preset} -c:a copy -movflags +faststart -y '
    command += f' "{temp_output_path_video}"'
    print(f"生成动态缩略图指令：{command}")
    subprocess.call(command, shell=True)

    threading.Thread(
        target=move_with_optional_security,
        args=(
            temp_output_path_video,
            output_path_video,
            os.path.join(os.path.dirname(temp_output_path_video), os.path.basename(output_path_video)),
            "视频缩略图移动到目标目录完毕...",
        ),
    ).start()
    for f in footage_paths:
        os.remove(f)


def gen_info(video_path, rows, cols):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise UserWarning("无法打开视频文件!")

    height, width, _ = cap.read()[1].shape
    if cols is None:
        # rows = math.ceil(((width / height) / (16 / 9 * 2) + 1 / 2) * rows)
        cols_precise = 16 * height * rows / 9 / width
        print(f"原始列数计算结果：{cols_precise}")
        if abs(round(cols_precise) - cols_precise) < 0.1:
            cols = round(cols_precise)
        else:
            cols = int(cols_precise)

    # 获取视频的总帧数和帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # 计算每个缩略图之间的帧间隔
    frame_interval = total_frames // (rows * cols)
    # 计算其他数据
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration_in_seconds = total_frames / fps
    cap.release()
    return frame_interval, fps, height, width, duration_in_seconds, rows, cols


def generate_thumbnail(video_path, rows, cols=None, preset="ultrafast", process_full_video=False, max_thumb_duration=30):
    def process_video(video_path, rows_calced, cols_calced, start_offset=0):
        frame_interval, fps, height, width, duration_in_seconds, _, _ = gen_info(video_path, rows_calced, cols_calced)
        gen_pic_thumbnail(video_path, frame_interval, rows_calced, cols_calced, height, width, start_offset)
        gen_video_thumbnail(
            video_path, preset, height, fps, duration_in_seconds, frame_interval, rows_calced, cols_calced, max_thumb_duration, start_offset
        )

    _, _, _, _, duration_in_seconds, rows_calced, cols_calced = gen_info(video_path, rows, cols)
    print(f"开始生成视频缩略图，视频路径：{video_path}，行列数：{rows_calced}x{cols_calced}")
    if process_full_video and rows_calced * cols_calced * max_thumb_duration < duration_in_seconds:
        n = 1
        seg_start_time = 0
        while seg_start_time < duration_in_seconds:
            seg_end_time = min(seg_start_time + rows_calced * cols_calced * max_thumb_duration, duration_in_seconds)
            seg_file_path = f"-seg{str(n).zfill(2)}".join(os.path.splitext(video_path))
            command = f'ffmpeg -ss {seg_start_time} -to {seg_end_time} -accurate_seek -i "{video_path}" -c copy -map_chapters -1 -y -avoid_negative_ts 1 "{seg_file_path}"'
            subprocess.run(command, shell=True)
            process_video(seg_file_path, rows_calced, cols_calced, start_offset=round(seg_start_time))
            seg_start_time = seg_end_time
            n += 1
    else:
        process_video(video_path, rows_calced, cols_calced)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video_path", help="视频路径或视频目录路径，如果不提供的话，则进入循环模式", type=str, nargs="?")
    parser.add_argument("rows", help="缩略图行数", type=int, nargs="?")
    parser.add_argument("cols", help="缩略图列数", type=int, nargs="?")
    parser.add_argument(
        "--preset",
        help="ffmpeg的preset参数",
        type=str,
        default="ultrafast",
        choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
    )
    parser.add_argument("--full", help="是否要生成多个缩略图以覆盖视频完整时长", action="store_true")
    parser.add_argument("-m", "--max", help="指定生成单个视频缩略图的最大时长", type=int, default=30)
    args = parser.parse_args()

    def process_video(args):
        video_path = args.video_path
        if (args.rows is None) and (args.cols is None):
            rows = 7
            cols = 7
        elif args.cols is None:
            rows = args.rows
            cols = None
        else:
            rows = args.rows
            cols = args.cols

        if os.path.isdir(video_path):
            video_paths = [
                os.path.join(video_path, f)
                for f in os.listdir(video_path)
                if os.path.splitext(f)[-1].lower()
                in [".mp4", ".flv", ".avi", ".mpg", ".wmv", ".mpeg", ".mov", ".mkv", ".ts", ".rmvb", ".rm", ".webm"]
            ]
            for video_path in video_paths:
                try:
                    generate_thumbnail(video_path, rows, cols, args.preset)
                except:
                    traceback.print_exc()
        elif str(video_path).lower().startswith("http"):
            file_name = os.path.basename(video_path)
            file_path = os.path.join(str(Path.home() / "Downloads"), file_name)
            if not os.path.exists(file_path):
                print(f"视频在本地不存在，开始下载: {file_name}")
                with open(file_path, "wb") as f:
                    f.write(requests.get(video_path, proxies={"http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"}).content)
            generate_thumbnail(file_path, rows, cols, args.preset)
        else:
            generate_thumbnail(video_path, rows, cols, args.preset, args.full, args.max)

    if args.video_path is None:
        while True:
            input_string = input("请输入视频地址和行数，以空格隔开：")
            if not input_string:
                continue
            video_path, rows_input = input_string.rsplit(" ", 1)
            try:
                rows = int(rows_input)
                cols = None
            except ValueError:
                rows, cols = [int(i) for i in rows_input.split("-")]
            threading.Thread(
                target=process_video,
                args=(
                    SimpleNamespace(
                        video_path=video_path.strip('"'),
                        rows=rows,
                        cols=cols,
                        preset=args.preset,
                        full=args.full,
                        max=args.max,
                    ),
                ),
            ).start()
    else:
        process_video(args)
