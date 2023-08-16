from whisper.utils import WriteSRT, WriteTXT
import os


DEFAULT_WRITER_CONFIG = {
    "highlight_words": False,
    "max_line_count": None,
    "max_line_width": None,
}


def _get_paths(output_file_path):
    output_dir = os.path.dirname(output_file_path)
    media_path_without_ext = os.path.splitext(output_file_path)[0]
    return output_dir, media_path_without_ext


def write_srt(result, output_file_path):
    output_dir, media_path_without_ext = _get_paths(output_file_path)
    writer = WriteSRT(output_dir)
    writer(result, media_path_without_ext, DEFAULT_WRITER_CONFIG)


def write_txt(result, output_file_path):
    output_dir, media_path_without_ext = _get_paths(output_file_path)
    writer = WriteTXT(output_dir)
    writer(result, media_path_without_ext, DEFAULT_WRITER_CONFIG)
