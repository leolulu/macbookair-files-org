import subprocess
from time import sleep
from typing import List, Optional

import requests

from utils import establish_temp_proxy_server, kill_subprocess_recursively, test_by_website, test_by_website_with_retry


class ProxyServerEstablisher:
    def __init__(self) -> None:
        self.p: Optional[subprocess.Popen] = None
        self.links: List[str] = []
        self.test_website_url = "https://www.youtube.com"

    def get_links(self):
        url = "http://43.139.10.228:1127/Saladict/filtered_node.txt"
        links = requests.get(url).text.split("\n")
        self.links = [i.strip() for i in links if i.startswith("vmess")]

    def run(self):
        while True:
            self.get_links()
            print(f"已获取新节点，共有【{len(self.links)}】个...")
            idx = 0
            while idx < len(self.links):
                link = self.links[idx]
                p = establish_temp_proxy_server(link, print_command=False, log_to_file=True)
                print(f"新建server，使用【{idx}】号link...")
                if test_by_website_with_retry(self.test_website_url, 5, 1):
                    print(f"节点初始测试成功...")
                    while True:
                        sleep(5)
                        if test_by_website(self.test_website_url):
                            # print(f"【日常检测】,正常运行中...")
                            pass
                        else:
                            print(f"【日常检测】,检测失败...")
                            kill_subprocess_recursively(p)
                            idx = 0
                            break
                else:
                    print(f"节点初始测试失败...")
                    kill_subprocess_recursively(p)
                    idx += 1
            print(f"所有的节点都失效了，获取新节点，开始下一轮...")


if __name__ == "__main__":
    pse = ProxyServerEstablisher()
    pse.run()
