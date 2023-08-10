import os
import sys

import cv2
import numpy as np
import uuid


def generate_thumbnail(video_path, rows, cols):
    # 读取视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise UserWarning("无法打开视频文件!")

    print(f"开始生成视频缩略图，视频路径：{video_path}，行列数：{rows}x{cols}")

    # 获取视频的总帧数和帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # 计算每个缩略图之间的帧间隔
    frame_interval = total_frames // (rows * cols)

    thumbnails = []

    for i in range(rows * cols):
        # 定位到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
        ret, frame = cap.read()

        if ret:
            # 计算时间戳
            seconds = (i * frame_interval) / fps
            hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            timestamp = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

            # 在图像的右上角添加时间戳（包括轮廓）
            cv2.putText(frame, timestamp, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 12)
            cv2.putText(frame, timestamp, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 6)

            thumbnails.append(frame)

    cap.release()

    # 计算缩略图的大小
    height, width, _ = thumbnails[0].shape
    thumbnail_width = width * cols
    thumbnail_height = height * rows

    # 创建一个空白的背景图像
    thumbnail = np.zeros((thumbnail_height, thumbnail_width, 3), dtype=np.uint8)

    # 将每个缩略图放置到背景图像上
    for i in range(rows):
        for j in range(cols):
            thumbnail[i * height : (i + 1) * height, j * width : (j + 1) * width, :] = thumbnails[i * cols + j]

    # 保存缩略图
    output_path = os.path.splitext(video_path)[0] + ".jpg"
    temp_output_path = os.path.join(os.path.dirname(video_path), f"{uuid.uuid4().hex}.jpg")
    print(f"缩略图保存路径为：{output_path}")
    cv2.imwrite(temp_output_path, thumbnail)
    os.rename(temp_output_path, output_path)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        video_path = sys.argv[1]
        rows = 10
        cols = 10
    elif len(sys.argv) == 4:
        video_path = sys.argv[1]
        rows = int(sys.argv[2])
        cols = int(sys.argv[3])
    else:
        raise UserWarning("参数错误！要么只提供视频路径，要么同时提供视频路径和行列数！")
    generate_thumbnail(video_path, rows, cols)
