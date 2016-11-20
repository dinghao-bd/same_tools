# coding:utf8

import mp3play
import time
import multiprocessing
import os
from eyed3.id3 import Tag
import eyed3

# PATH = "F:\music"
PATH = "d:\mp3"
BACKUP_PATH = "d:\mp3_backup"


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
        # close = multiprocessing.Process(target=self.close())
        # close.start()
        # close.join()

    # def close(self):
    #     time.sleep(10)
    #     self.fd.close()

    def play_time(self):
        """
        返回播放时间
        :return:
        """
        for i in xrange(self.seconds):
            self.return_time(i)
            time.sleep(1)

    def return_time(self, time):
        print "当前时间：%s，总时间：%s" % (time, self.seconds)

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

    def stop(self):
        pass

    def next_song(self):
        pass

    def parser_mp3(self):
        tag = Tag()
        tag.remove(self.file_path)

    def is_id3(self):
        self.fd.seek(0)
        head = self.fd.read(3)
        if head == "ID3":
            return True
        else:
            return False

    def get_name(self):
        pass

    def get_pid(self):
        pass

    def time_of_song(self):
        return self.seconds


def get_file_list(path):
    file_path = []
    for dir_path, dir_name, file_names in os.walk(path):
        for file_name in file_names:
            file_path.append(os.path.join(dir_path, file_name))
    return file_path


def is_mp3(file_path):
    return os.path.splitext(file_path)[-1] == ".mp3"


if __name__ == '__main__':

    for path in get_file_list(PATH):
        print path
        if is_mp3(path):
            mp3 = MP3(path)
            mp3.run()

    # mp3 = MP3(mp3_list)

    # print "1：播放歌曲，2：暂停，3：下一曲，4：停止"
    # numb = int(raw_input("请输入指令："))
    # while True:
    #     if numb is 1:
    #         mp3.run()
    #     if numb is 2:
    #         pass
