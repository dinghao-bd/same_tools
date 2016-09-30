#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1
@author: ding hao
@license: Apache Licence 
@file: toast_service.py
@time: 2016/9/26 16:45
"""

import multiprocessing
import time
import subprocess
from uiautomator import Device

d = Device("b88b8da")


class ToastService():
    """
    执行命令：adb shell uiautomator events 抓取accessbility 的内容，然后分析内容，取得toast
    """

    def check_toast(self, item, toast):
        item_bounds = self.get_bounds(item)
        d.server.stop()
        subprocess.Popen('adb shell uiautomator events > events.txt', shell=True)
        time.sleep(1)
        self.tap_item(item_bounds)
        time.sleep(5)
        if self.check_toast_in_events(toast) is True:
            subprocess.Popen("adb kill-server", shell=True)
            time.sleep(1)
            subprocess.Popen("adb start-server", shell=True)
            d.server.start()
            return True
        else:
            d.server.start()
            return False

    def check_toast_in_events(self, toast):
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
        bounds_json = item.info["bounds"]
        bounds_x = (bounds_json["left"] + bounds_json["right"]) / 2
        bounds_y = (bounds_json["top"] + bounds_json["bottom"]) / 2
        return bounds_x, bounds_y

    def tap_item(self, item_bounds):
        tap_cmd = "adb shell input tap %d %d" % item_bounds
        print tap_cmd
        subprocess.Popen(tap_cmd, shell=True)


# toast_service = ToastService()

if __name__ == '__main__':
    toast_service = ToastService()
    toast_service.check_toast(d(resourceId="com.zhangyue.iReader.search:id/search_view__head_view__search_icon"),
                              "您还未输入任何词语，请重新输入")


# os.remove('events.txt')
# child1 = subprocess.Popen('adb shell uiautomator events > events.txt', shell=True)
# time.sleep(10)
# child2 = subprocess.Popen('adb kill-server', shell=True)
# child3 = subprocess.Popen('adb start-server', shell=True)
#
# print 111
