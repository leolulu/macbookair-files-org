import json
import os
import pickle
import subprocess
import time
import traceback
from collections import deque

import requests


class ProxyNode:
    def __init__(self, link) -> None:
        self.link = link
        self.avg_speeds = deque(maxlen=10)
        self.fail_streak = 0
        self.name = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ProxyNode):
            return self.link == other.link
        return False

    def __hash__(self) -> int:
        return hash(self.link)

    def mark_fail_streak(self, isok: bool):
        if isok:
            self.fail_streak = 0
        else:
            self.fail_streak += 1

    @property
    def longterm_avg_speed(self):
        if not self.avg_speeds:
            return 0
        else:
            return int(sum(self.avg_speeds) / len(self.avg_speeds))

    @property
    def isok(self):
        return self.fail_streak == 0


class BLL_proxy_getter:
    def __init__(self, top_node_count=5) -> None:
        self.proxy = "http://127.0.0.1:10809"
        self.last_frame_file_name = "last.jpg"
        self.result_file_name = "filtered_node.txt"
        self.speed_test_output_file_name = "output.json"
        self.serialized_nodes_file_name = "proxy_nodes.pkl"
        if os.path.exists(self.result_file_name):
            os.remove(self.result_file_name)
        if os.path.exists(self.speed_test_output_file_name):
            os.remove(self.speed_test_output_file_name)
        if os.path.exists(self.serialized_nodes_file_name):
            with open(self.serialized_nodes_file_name, "rb") as f:
                self.proxy_nodes = pickle.loads(f.read())
        else:
            self.proxy_nodes = set()
        self.top_node_count = top_node_count

    def set_proxy(self):
        os.environ["http_proxy"] = self.proxy
        os.environ["https_proxy"] = self.proxy

    def unset_proxy(self):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

    def get_streaming_url(self):
        self.set_proxy()
        command = "yt-dlp -g uHue-U3ArfE | head -n 1"
        print(f"开始尝试获取直播视频地址...")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        self.unset_proxy()

        if process.returncode == 0:
            self.steaming_url = output.decode().strip()
            if not self.steaming_url:
                raise UserWarning(f"没有成功获取到视频地址：{error.decode().strip()}")
            print(f"获取到直播视频真地址：{self.steaming_url[:50]}...")
        else:
            print("Error:", error.decode().strip())
            self.steaming_url = None

    def get_last_frame(self):
        self.set_proxy()
        command = f'ffmpeg -hide_banner -loglevel error -i "{self.steaming_url}" -vframes 1 -y {self.last_frame_file_name}'
        print(f"开始尝试获取视频最后一帧，指令：\n{command[:100]}...")
        subprocess.run(command, shell=True)
        self.unset_proxy()

    def get_qr_data(self):
        url = "http://api.qrserver.com/v1/read-qr-code/"
        f = open(self.last_frame_file_name, "rb")
        files = {"file": f}
        response = requests.post(url, files=files)
        f.close()
        response.raise_for_status()
        link = json.loads(response.content)[0]["symbol"][0]["data"]
        self.deal_with_link(link)
        os.remove(self.last_frame_file_name)

    def deal_with_link(self, link: str):
        if link.lower().startswith("ss"):
            print(f"节点为ss系，跳过...")
            return
        if link.lower().startswith("trojan"):
            print(f"节点为trojan类型，跳过...")
            return
        print(f"获取到当前图像的二维码内容：\n{link}")
        self.proxy_nodes.add(ProxyNode(link))

    def find_node_by_link(self, link):
        for proxy_node in self.proxy_nodes:
            if proxy_node.link == link:
                return proxy_node
        return None

    def test_node_speed(self):
        if not self.proxy_nodes:
            print(f"节点池中没有节点，跳过测速环节...")
            return
        print(f"准备开始测速，当前节点池里面共有{len(self.proxy_nodes)}个节点...")

        for proxy_node in self.proxy_nodes:
            link_str = proxy_node.link
            command = f'lite-windows-amd64.exe -config config.json -test "{link_str}" >nul 2>&1'
            print(f"开始测速，指令：\n{command[:100]}...")
            try:
                subprocess.run(command, shell=True, timeout=180)
                with open("output.json", "r", encoding="utf-8") as f:
                    all_result = json.loads(f.read())
                for node_result in all_result["nodes"]:
                    proxy_node = self.find_node_by_link(node_result["link"])
                    if proxy_node:
                        isok = node_result["isok"]
                        proxy_node.mark_fail_streak(isok)
                        if isok:
                            proxy_node.avg_speeds.append(node_result["avg_speed"])
                        if not proxy_node.name:
                            proxy_node.name = node_result["remarks"]
                        break
                    else:
                        print(f"[DEBUG]竟然有link在node库里面找不到，奇了个怪了...")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                print(f"测速超时，跳过当前节点本轮测速，标记测速失败...{e}")
                node = self.find_node_by_link(link_str)
                if node:
                    node.mark_fail_streak(False)
                else:
                    print(f"[DEBUG]无法通过link匹配节点...")

        nodes_to_remove = []
        for proxy_node in self.proxy_nodes:
            if proxy_node.fail_streak >= 10:
                nodes_to_remove.append(proxy_node)
        for node_to_remove in nodes_to_remove:
            self.proxy_nodes.remove(node_to_remove)

        top_nodes = sorted([i for i in self.proxy_nodes if i.isok], key=lambda x: x.longterm_avg_speed, reverse=True)[: self.top_node_count]
        if top_nodes:
            result_output_content = "{}\n\n{}\n\n更新时间: {}".format(
                "\n".join([i.link for i in top_nodes]),
                "\n".join([f"{round(i.longterm_avg_speed/1024/1024,2)}MB/S - {i.name}" for i in top_nodes]),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            )
            with open(self.result_file_name, "w", encoding="utf-8") as f:
                f.write(result_output_content)

        os.remove(self.speed_test_output_file_name)

    def save_nodes(self):
        if self.proxy_nodes:
            serialized_obj = pickle.dumps(self.proxy_nodes)
            with open(self.serialized_nodes_file_name, "wb") as file:
                file.write(serialized_obj)

    def send_result_file_to_dufs(self):
        url = f"http://42.193.43.79:1127/Saladict/{self.result_file_name}"
        with open(self.result_file_name, "rb") as f:
            response = requests.put(url, data=f)
            response.raise_for_status()
        print(f"测速完毕，结果已保存...\n")

    def run(self):
        self.get_streaming_url()
        self.get_last_frame()
        self.get_qr_data()
        self.test_node_speed()
        self.save_nodes()
        self.send_result_file_to_dufs()


if __name__ == "__main__":
    round_interval = 600
    top_node_count = 5
    bll = BLL_proxy_getter(top_node_count=top_node_count)
    while True:
        last_btime = time.time()
        try:
            bll.run()
        except:
            traceback.print_exc()
        while time.time() - last_btime < (30 if len(bll.proxy_nodes) < top_node_count else round_interval):
            print(f"等待下一轮测速，剩余时间：{int(round_interval - (time.time() - last_btime))}秒...")
            time.sleep(10)
