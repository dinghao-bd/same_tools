# coding:utf8
import os
import time
import sys
import threading

class adb_tools(object):

    TIME_OUT = 3
    
    def __init__(self):
        pass

    def get_devices_list(self):
        cmd = "adb devices"
        devices_list=[]
        device_list = os.popen(cmd).readlines()
        for device in device_list:
            if device == "List of devices attached\\n" or device.find("offline")== 0:
                continue
            if device.find("device")==0:
                devices_list.append(device[:-8])
        return devices_list

    def push_file(self, sources, destination, serial=None):
        device_serial = self.__check_device(serial)
        cmd = "adb -s %s push %s %s",(device_serial,sources,destination)
        paths = os.popen(cmd).readlines()
        for path in paths:
            if destination == path:
                return True
            else:
                return False

    def get_screencap(self, path, serial=None):
        device_serial = self.__check_device(serial)
        cmd_cap = "adb -s %s shell screencap /sdcard/cap.png",device_serial

    def pull_file(self, sources, destination, serial=None):
        '''
        :param sources:
        :param destination:
        :param serial:
        :return:
        TODO: check results
        '''
        device_serial = self.__check_device(serial)
        cmd = "adb -s %s pull %s %s",(device_serial,sources,destination)
        paths = os.popen(cmd).readlines()
        for path in paths:
            if destination == path:
                return True
            else:
                return False



    def get_log(self):
        pass

    def install_pkg(self):
        pass

    def uninstall_pkg(self):
        pass


    def __check_device(self,serial):
        device=self.get_devices_list
        if len(device)<=1:
            if serial==None:
                return device[0]
            else:
                return serial
        elif(serial == None):
            raise AttributeError,"超过一个设备，请指定序列号！"
        else:
            pass


    # def __getcmd(self,shell):
    #     return os.popen(shell)

    def __get_platform(self):
        '''
        :return: 1表示 windows ，2表示Linux/Unix，3表示其他系统
        '''
        if os.name=="nt":
            return 1
        elif os.name=="posix":
            return 2
        else:
            return 3



class exc_threading(threading.Thread):

    def __init__(self,name,num):
        super(exc_threading,self).__init__(name=name)
        self.num = num
        self.thread_stop = False

    def run(self):
        while num or not self.thread_stop:
            pass



    def stop(self):
        self.thread_stop = True



adb_tools = adb_tools()