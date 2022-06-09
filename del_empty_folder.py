import os
import re

remove_files = ['谨防被骗.png', 'RARBG.txt', 'RARBG_DO_NOT_MIRROR.exe']
remove_types = ['.nfo']


def del_empty_folder(folder_path):
    file_count = 0
    nonempty_folder_count = 0
    for i in os.listdir(folder_path):
        i = os.path.join(folder_path, i)
        if os.path.isfile(i):
            if re.match(r"^\.", os.path.basename(i).lower()):
                os.remove(i)
                print('删除隐藏文件：', i)
                continue
            if os.path.basename(i) in remove_files:
                os.remove(i)
                print('删除文件：', i)
                continue
            if os.path.splitext(i)[-1] in remove_types:
                os.remove(i)
                print('删除类型：', i)
                continue
        if os.path.isfile(i):
            file_count += 1
        if os.path.isdir(i):
            nonempty_folder_count += del_empty_folder(i)
    if file_count == 0 and nonempty_folder_count == 0:
        os.rmdir(folder_path)
        print('删除空目录：', folder_path)
        return 0
    else:
        return 1


if __name__ == "__main__":
    import sys
    del_empty_folder(sys.argv[1])
