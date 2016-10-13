# coding:utf8

import mp3play
import time
import multiprocessing


class MP3(object):
    def __init__(self, file_path):
        self.file_path = file_path
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

    def get_pid(self):
        pass

    def time_of_song(self):
        return self.seconds


if __name__ == '__main__':
    file_path = ["D:\\MP3\\LoveStory.mp3","D:\\MP3\\xiangaihengzao.mp3", "D:\\MP3\\foshuo.mp3", ]
    for path in file_path:
        mp3 = MP3(path)
        mp3.run()
        # time.sleep(mp3.time_of_song())
