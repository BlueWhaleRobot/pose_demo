#encoding=utf-8
#!/usr/bin/python
"""
获取当前局域网内所有巡检机器人位置。每个机器人都会通过UDP广播在局域网内广播自己的配置信息。
获取信息后连接机器人的IP，通过http协议获取具体每个机器人的位置
"""

import socket
import thread
import threading
import requests
import json
import time

host = '0.0.0.0'
port = 49204

ROBOTS = {}
ROBOTS_LOCK = threading.RLock()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

def update_robot_info():
    global ROBOTS
    while True:
        try:
            message, address = s.recvfrom(8192)
            robot_info = json.loads(message)
            with ROBOTS_LOCK:
                if robot_info['id'] not in ROBOTS:
                    ROBOTS[robot_info['id']] = robot_info
                    ROBOTS[robot_info['id']]['ip'] = address[0]

        except (KeyboardInterrupt, SystemExit):
            break

thread.start_new_thread(update_robot_info, ())

if __name__ == "__main__":
    while True:
        print("##########################################################")
        with ROBOTS_LOCK:
            for robot in ROBOTS:
                res = None
                try:
                    res = requests.get(
                        "http://{ip}:{port}/api/v1/navigation/pose".format(
                            ip=ROBOTS[robot]["ip"],
                            port=ROBOTS[robot]["port"]
                        ))
                    res = json.loads(res.content.decode("utf-8"))
                except:
                    continue
                ROBOTS[robot]["pose"] = res
                print("ID: {robot_id} x: {x} y: {y} angle: {angle}".format(
                    robot_id=ROBOTS[robot]['id'][:8],
                    x=ROBOTS[robot]["pose"]['x'],
                    y=ROBOTS[robot]["pose"]['y'],
                    angle=ROBOTS[robot]["pose"]['angle'],
                ))

        time.sleep(1)
