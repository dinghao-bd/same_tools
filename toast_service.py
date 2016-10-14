#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@mail: 619015618@qq.com
@file: toast_service.py
@time: 2016/9/26 16:45
"""

import time
import os
import subprocess
from uiautomator import Device as d


class ToastService():
    """
    执行命令：adb shell uiautomator events 抓取accessbility 的事件，然后分析内容，取得toast
    由于events不能和runtests同时运行，所以在运行events时，要先关闭runtests
    """

    def check_toast(self, item, toast):
        item_bounds = self.get_bounds(item)
        d.server.stop()
        subprocess.Popen('adb shell uiautomator events > events.txt', shell=True)
        time.sleep(1)
        self.tap_item(item_bounds)
        time.sleep(5)
        if self.check_toast_in_events(toast) is True:
            self.remove_events()
            d.server.start()
            return True
        else:
            self.remove_events()
            d.server.start()
            return False

    def remove_events(self):
        # TODO: 查询adb是否会有多个进程，然后根据进程ID进行kill，避免误杀
        subprocess.Popen("adb kill-server", shell=True)
        os.remove("events.txt")

    def get_pid(self, name):
        cmd = "ps aux | grep '%s' " % name
        child1 = subprocess.Popen(cmd, shell=True)
        info = child1.stdout.split()
        if len(info) > 1:
            return info[1]
        else:
            return -1

    def check_toast_in_events(self, toast):
        """
        在events中，查询有没有符合toast的内容
        :param toast:
        :return:
        """
        with open("events.txt", "r") as f:
            contents = f.readlines()
            for content in contents:
                print content
                if toast in content:
                    return True
                else:
                    continue
            return False

    def get_bounds(self, item):
        """
        获取控件的坐标
        :param item:
        :return: 返回控件的坐标
        """
        bounds_json = item.info["bounds"]
        bounds_x = (bounds_json["left"] + bounds_json["right"]) / 2
        bounds_y = (bounds_json["top"] + bounds_json["bottom"]) / 2
        return bounds_x, bounds_y

    def tap_item(self, item_bounds):
        """
        点击控件
        :param item_bounds:
        :return:
        """
        tap_cmd = "adb shell input tap %d %d" % item_bounds
        subprocess.Popen(tap_cmd, shell=True)


# toast_service = ToastService()
if __name__ == '__main__':
    toast_service = ToastService()
    toast_service.get_pid("chrome")