import base64
import json
import subprocess
from time import sleep
from typing import Any, Dict, List

import psutil
import requests


def kill_subprocess_recursively(p: subprocess.Popen):
    process = psutil.Process(p.pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def establish_temp_proxy_server_with_multiple_links(
    links: List[str],
    v2ray_config_template_file_name,
    v2ray_config_file_name,
    log_file_name,
    log_to_file=False,
    print_command=False,
):
    def parse_link(link) -> Dict[str, Any]:
        link_info = json.loads(base64.b64decode(link.replace("vmess://", "")).decode("utf-8"))
        if link_info["type"] != "none" or link_info["tls"] != "":
            print(link_info)
            raise UserWarning("遇到不支持解析的config...")
        return link_info

    links_info = [parse_link(l) for l in links]
    with open(v2ray_config_template_file_name, "r", encoding="utf-8") as f:
        v2ray_config = json.loads(f.read().strip())
    outbound_info = v2ray_config["outbounds"][0]
    vnext = []
    for link_info in links_info:
        vnext.append(
            {
                "address": link_info["add"],
                "port": int(link_info["port"]),
                "users": [
                    {
                        "id": link_info["id"],
                        "alterId": int(link_info["aid"]),
                        "security": "auto",
                    }
                ],
            }
        )
    outbound_info["settings"]["vnext"] = vnext
    outbound_info["streamSettings"]["network"] = list(set([i["net"] for i in links_info]))[0]
    v2ray_config["outbounds"] = [outbound_info]
    with open(v2ray_config_file_name, "w", encoding="utf-8") as f:
        f.write(json.dumps(v2ray_config, indent=2))

    command = f"v2ray.exe -config {v2ray_config_file_name} "
    if log_to_file:
        command += f' >> "{log_file_name}" 2>&1'
    if print_command:
        print(command)
    return subprocess.run(command, shell=True)


def establish_temp_proxy_server(
    link: str,
    v2ray_config_template_file_name,
    v2ray_config_file_name,
    log_file_name,
    log_to_file=False,
    print_command=False,
):
    link_info = json.loads(base64.b64decode(link.replace("vmess://", "")).decode("utf-8"))
    if link_info["type"] != "none" or link_info["tls"] != "":
        print(link_info)
        raise UserWarning("遇到不支持解析的config...")
    with open(v2ray_config_template_file_name, "r", encoding="utf-8") as f:
        v2ray_config = json.loads(f.read().strip())
    outbound_info = v2ray_config["outbounds"][0]
    outbound_info["settings"]["vnext"] = [
        {
            "address": link_info["add"],
            "port": int(link_info["port"]),
            "users": [
                {
                    "id": link_info["id"],
                    "alterId": int(link_info["aid"]),
                    "security": "auto",
                }
            ],
        }
    ]
    outbound_info["streamSettings"]["network"] = link_info["net"]
    v2ray_config["outbounds"] = [outbound_info]
    with open(v2ray_config_file_name, "w", encoding="utf-8") as f:
        f.write(json.dumps(v2ray_config, indent=2))

    command = f"v2ray.exe -config {v2ray_config_file_name} "
    if log_to_file:
        command += f' >> "{log_file_name}" 2>&1'
    if print_command:
        print(command)
    return subprocess.Popen(command, shell=True)


def test_by_website(
    test_website_url,
    proxy_str=f"http://127.0.0.1:10809",
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
