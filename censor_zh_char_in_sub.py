import re
import sys
import os


def censor_zh_char(text):
    result = re.sub(r'([\u4e00-\u9fa5]+(?:[\s\-·\?!？！,\.，。0-9"“”]+[\u4e00-\u9fa5]+)*)', r'<span class="censored">\1</span>', text)
    return result


if __name__ == "__main__":
    text_file_path = sys.argv[1]
    censor_text_file_path = "_censored".join(os.path.splitext(text_file_path))
    with open(text_file_path, "r", encoding="utf-8") as f:
        text = f.read()
    with open(censor_text_file_path, "w", encoding="utf-8") as f:
        f.write(censor_zh_char(text))
