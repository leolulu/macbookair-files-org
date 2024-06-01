import os
import subprocess
import sys
import traceback


def extract_audio(video_file_path):
    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_file_path,
    ]
    codec_output = subprocess.check_output(ffprobe_cmd).decode().strip()

    if codec_output == "aac":
        audio_extension = ".aac"
    elif codec_output == "mp3":
        audio_extension = ".mp3"
    elif codec_output == "opus":
        audio_extension = ".opus"
    elif codec_output == "vorbis":
        audio_extension = ".ogg"
    elif codec_output == "flac":
        audio_extension = ".flac"
    elif codec_output == "pcm_s16le":
        audio_extension = ".wav"
    else:
        raise UserWarning(f"不支持的音频编码格式: {codec_output}")

    output_audio_path = os.path.splitext(video_file_path)[0] + audio_extension
    ffmpeg_cmd = ["ffmpeg", "-i", video_file_path, "-vn", "-acodec", "copy", output_audio_path]
    subprocess.call(ffmpeg_cmd)


if __name__ == "__main__":
    input_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(input_path):
        for i in os.listdir(input_path):
            input_path_ = os.path.join(input_path, i)
            print(f"开始处理: {input_path_}")
            try:
                extract_audio(input_path_)
            except:
                traceback.print_exc()
    else:
        extract_audio(input_path)
