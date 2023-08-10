import os


def change_ext(file_path, ext: str, postfix=None):
    file_, ext = os.path.splitext(file_path)
    if not ext.startswith("."):
        ext = "." + ext
    if postfix:
        return file_ + "_" + postfix + ext
    else:
        return file_ + ext
