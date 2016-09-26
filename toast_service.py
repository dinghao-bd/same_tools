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


class ToastService(multiprocessing.Process):
    """
    执行命令：adb shell uiautomator events 抓取accessbility 的内容，然后分析内容，取得toast
    """
    def __init__(self):
        super(ToastService).__init__(self)

    def parse_content(self, content):
        pass

    def run(self):
        pass
