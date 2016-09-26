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
from uiautomator import device as d





# class ToastService(multiprocessing.Process):
#     """
#     执行命令：adb shell uiautomator events 抓取accessbility 的内容，然后分析内容，取得toast
#     """
#
#     #
#     # def __init__(self):
#     #     super(ToastService).__init__(self)
#
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
#         super(ToastService, self).__init__(group=None, target=None, name=None, args=(), kwargs={})
#         cmd = "adb shell uiautomator events"
#
#         self.child = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#         self.child.wait()
#         print self.child.stdout.read()
#
#     def parse_content(self):
#         # with open('events.txt', 'r') as f:
#         #     print f.readline()
#         pass
#
#
# if __name__ == '__main__':
#     toast_service = ToastService()
#     toast_service.parse_content()
child1 = subprocess.Popen('adb shell uiautomator events', shell=True, stdout=subprocess.PIPE)
print child1.stdout.read()