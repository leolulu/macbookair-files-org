import subprocess
from time import sleep

import psutil
import requests

default_temp_proxy_server_port = 10808


def kill_subprocess_recursively(p: subprocess.Popen):
    process = psutil.Process(p.pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def establish_temp_proxy_server(
    link: str,
    temp_proxy_server_port=default_temp_proxy_server_port,
    log_to_file=False,
    log_file_name="temp_proxy_server_for_local_proxy.log",
    print_command=False,
):
    command = f'lite-windows-amd64.exe -p {temp_proxy_server_port} "{link}"'
    if log_to_file:
        command += f' >> "{log_file_name}" 2>&1'
    if print_command:
        print(command)
    return subprocess.Popen(command, shell=True)


def test_by_website(
    test_website_url,
    proxy_str=f"http://127.0.0.1:{default_temp_proxy_server_port}",
    print_exception=False,
):
    try:
        proxies = {"http": proxy_str, "https": proxy_str}
        response = requests.get(test_website_url, proxies=proxies, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        if print_exception:
            print(e)
        return False


def test_by_youtube(proxy_str):
    return test_by_website("https://www.youtube.com/", proxy_str=proxy_str)


def test_by_website_with_retry(test_website_url, max_retry=5, retry_interval=1):
    fail_times = 0
    while fail_times <= max_retry:
        if test_by_website(test_website_url):
            return True
        else:
            fail_times += 1
            sleep(retry_interval)
    return False
