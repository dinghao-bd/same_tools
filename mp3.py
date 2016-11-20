# coding:utf8

import mp3play
import time
import multiprocessing
import os
from eyed3.id3 import Tag


class MP3(object):
    def __init__(self, file_path):

        self.file_path = file_path
        self.fd = open(file_path)
        if self.is_id3():
            self.parser_mp3()
            self.seconds = mp3play.load(self.file_path).seconds()
        else:
            self.seconds = mp3play.load(self.file_path).seconds()

    def play(self):
        """
        播放音频文件
        :return:
        """
        mp3 = mp3play.load(self.file_path)
        mp3.play()
        sleep_time = min(1800, mp3.seconds())
        time.sleep(sleep_time + 3)
        mp3.stop()
        self.close()

    def close(self):
        """
        关闭打开的文件
        :return:
        """
        if not self.fd.closed:
            self.fd.close()

    def play_time(self):
        """
        返回播放时间
        :return:
        """
        for i in xrange(self.seconds):
            self.return_time(i)
            time.sleep(1)

    def return_time(self, time):
        """
        返回播放时间
        :param time:
        :return:
        """
        return "当前时间：%s，总时间：%s" % (time, self.seconds)

    def run(self):
        jobs = []
        player = multiprocessing.Process(target=self.play)
        print_play_time = multiprocessing.Process(target=self.play_time)
        jobs.append(player)
        jobs.append(print_play_time)
        for job in jobs:
            job.start()
        for job in jobs:
            job.join()

    def parser_mp3(self):
        """
        处理mp3的head部分
        :return:
        """
        tag = Tag()
        tag.remove(self.file_path)

    def is_id3(self):
        """
        判断是不是新的head，也就是MP3 v2 id3
        :return:
        """
        self.fd.seek(0)
        head = self.fd.read(3)
        if head == "ID3":
            return True
        else:
            return False


def get_file_list(path):
    """
    获取文件夹中的文件路径列表
    :param path:
    :return:
    """
    file_path = []
    for dir_path, dir_name, file_names in os.walk(path):
        for file_name in file_names:
            file_path.append(os.path.join(dir_path, file_name))
    return file_path


def is_mp3(file_path):
    """
    根据后缀名判断是不是mp3文件
    :param file_path:
    :return:
    """
    return os.path.splitext(file_path)[-1] == ".mp3"


if __name__ == '__main__':
    PATH = ""
    for path in get_file_list(PATH):
        print path
        if is_mp3(path):
            mp3 = MP3(path)
            mp3.run()
