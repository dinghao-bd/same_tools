# coding:utf8

import mp3play
import time
import multiprocessing
import os

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

    def parser_mp3(self):
        pass
        # 备份文件，还有需要去掉head部分
        os.rename(self.file_path, self.file_path.replace(PATH, BACKUP_PATH))

        file = open(self.file_path)

    def is_id3(self):
        self.fd.seek(0)
        head = self.fd.read(3)
        if head == "ID3":
            return True
        else:
            return False

    def get_id3_ver2_size(self):
        length = 4
        self.fd.seek(6, os.SEEK_SET)
        size = self.fd.read(length)
        total_size = (ord(size[0]) & 0x7f) * 0x2000000 + (ord(size[1]) & 0x7f) * 0x40000 + \
                     (ord(size[2]) & 0x7f) * 0x80 + ord(size[3]) & 0x7f
        return total_size

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
    return os.path.splitext(file_path)[-1] == "mp3"


if __name__ == '__main__':

    for path in get_file_list(PATH):
        if is_mp3(path):
            mp3 = MP3(path)
            # mp3.run()
