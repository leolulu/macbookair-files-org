import os
import subprocess
from time import sleep
from typing import List, Optional

import requests

from utils import (
    establish_temp_proxy_server,
    kill_subprocess_recursively,
    test_by_website,
    test_by_website_with_retry,
    establish_temp_proxy_server_with_multiple_links,
    establish_temp_proxy_server_with_v2fly,
)


class Link:
    def __init__(self, link: str) -> None:
        self.link = link
        self.fail_times = 0

    def fail(self):
        self.fail_times += 1


class Links:
    def __init__(self) -> None:
        self.init_links()

    def init_links(self):
        url = "http://43.139.10.228:1127/Saladict/filtered_node.txt"
        links = requests.get(url).text.split("\n")
        links = [i.strip() for i in links if i.startswith("vmess")]
        self.raw_links: List[str] = links
        self.links: List[Link] = [Link(l) for l in links]
        print(f"已获取新节点，共有【{len(self.links)}】个...")

    def get_one(self):
        if min(self.links, key=lambda x: x.fail_times).fail_times >= 5:
            self.init_links()
        return min(self.links, key=lambda x: x.fail_times)

    def get_all(self):
        return self.raw_links


class ProxyServerEstablisher:
    def __init__(self) -> None:
        self.p: Optional[subprocess.Popen] = None
        self.links: Links = Links()
        self.test_website_url = "https://www.youtube.com"
        self.v2ray_config_template_file_name = "v2ray_config.template"
        self.v2ray_config_file_name = "v2ray_config.json"
        self.log_file_name = "temp_proxy_server_for_local_proxy.log"
        self.init_local_files()

    def init_local_files(self):
        if os.path.exists(self.v2ray_config_file_name):
            os.remove(self.v2ray_config_file_name)
        if os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)

    def run(self):
        while True:
            link = self.links.get_one()
            p = establish_temp_proxy_server(
                link.link,
                self.v2ray_config_template_file_name,
                self.v2ray_config_file_name,
                self.log_file_name,
                print_command=False,
                log_to_file=True,
            )
            print(f"新建server，当前links的fail情况为: {[l.fail_times for l in self.links.links]}")
            if test_by_website_with_retry(self.test_website_url, 5, 1):
                print(f"节点初始测试成功...")
                while True:
                    sleep(5)
                    if test_by_website(self.test_website_url):
                        pass
                    else:
                        for _ in range(3):
                            if test_by_website(self.test_website_url):
                                continue
                        print(f"【日常检测】,检测失败...")
                        kill_subprocess_recursively(p)
                        link.fail()
                        break
            else:
                print(f"节点初始测试失败...")
                kill_subprocess_recursively(p)
                link.fail()

    def run_with_all_links(self):
        establish_temp_proxy_server_with_multiple_links(
            self.links.get_all(),
            self.v2ray_config_template_file_name,
            self.v2ray_config_file_name,
            self.log_file_name,
            print_command=True,
            log_to_file=False,
        )

    def run_with_v2fly(self):
        establish_temp_proxy_server_with_v2fly(
            self.links.get_all(),
            self.v2ray_config_template_file_name,
            self.v2ray_config_file_name,
            self.log_file_name,
            print_command=True,
            log_to_file=False,
        )


if __name__ == "__main__":
    pse = ProxyServerEstablisher()
    pse.run_with_v2fly()
