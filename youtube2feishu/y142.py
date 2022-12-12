import subprocess
import sys

command = 'python yt_dlp_tool.py --dl_dir "{dl_dir}" --postprefix "__l0" {url}'.format(
    dl_dir=r"\\192.168.123.222\folder_for_142",
    url=sys.argv[1]
)
print(command)
subprocess.Popen(command)
