import os
import shutil
import subprocess
import sys


def gen_command(dir, name, max_size=float("inf")):
    command_template = 'python Images_To_ePub.py -c -d "{d}" -f "{f}" -n "{n}"'
    base_dir = os.path.abspath(dir)
    folder_idx = 1
    batch_pics_size = 0
    batch_info = []
    for pic_file_name in os.listdir(base_dir):
        pic_file_path = os.path.join(base_dir, pic_file_name)
        pic_file_size = os.path.getsize(pic_file_path) / 1024 / 1024
        if batch_pics_size + pic_file_size > max_size:
            folder_idx += 1
            batch_pics_size = 0
        current_batch_folder_path = os.path.join(base_dir, str(folder_idx))
        if not os.path.exists(current_batch_folder_path):
            os.mkdir(current_batch_folder_path)
            batch_info.append([folder_idx, current_batch_folder_path])
        shutil.move(pic_file_path, current_batch_folder_path)
        batch_pics_size += pic_file_size
    commands = []
    for idx, batch_folder_path in batch_info:
        commands.append(
            command_template.format(
                d=batch_folder_path,
                n=(n := f"{name}-{str(idx).zfill(2)}"),
                f=os.path.join(base_dir, f"{n}.epub"),
            )
        )
    print("指令生成: ")
    print(" & ".join(commands))
    print("\n指令运行: ")
    for cmd in commands:
        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        gen_command(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    elif len(sys.argv) == 3:
        gen_command(sys.argv[1], sys.argv[2])
    else:
        print(f"Usage: python gen_command.py pic_dir book_name [max_MB_per_epub]")
