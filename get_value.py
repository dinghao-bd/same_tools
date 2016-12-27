#!/usr/bin/python
# -*- coding:utf-8 -*- 

"""
@author: Ding Hao
"""
import os
import time
import commands


class GetValue(object):
    """docstring for getValue"""

    def __init__(self):
        pass
        # output = self.exc('adb devices')
        # serial = ''
        # output.remove(output[0])
        # for x in xrange(len(output)):
        #     output[x] = output[x][0:-8]
        #     if output[x] is '':
        #         output.remove(output[x])
        # if output:
        #     serial = output[0]
        # else:
        #     raise ValueError, 'device not found'

    def exc(self, shell, loop=3):
        if os.name == 'nt':
            loop = 1
            for x in xrange(0, loop):
                if os.name is 'nt':
                    output = os.popen(shell).readlines()
                    print output
                    if output:
                        return output
                elif os.name is 'posix':
                    (status, output) = commands.getstatusoutput(shell)
                    if status == 0:
                        return output

    def get_max_mem(self):
        """
        get max mem
        """

        max_mem = self.exc('adb shell getprop | findstr heapgrowthlimit')
        max_mem = max_mem[30:].replace('m]\r', '')
        return max_mem

    def getMeminfo(self):

        maminfo = self.exc('adb shell dumpsys meminfo com.zhangyue.iReader.Eink | findstr TOTAL')
        # return maminfo.replace('\r', '').split('    ')[6]
        return maminfo

    def delNoneElements(self, list1):

        lenght = len(list1)
        for x in xrange(0, lenght):
            i = len(list1[x]) - 1
            while i >= 0:
                if list1[x][i] == '':
                    del list1[x][i]
                    i = len(list1[x]) - 1
                else:
                    i -= 1
        return list1

    def getList(self, str1):

        list1 = str1.replace('\r', '').split('\n')
        lenght = len(list1)
        for x in xrange(0, lenght):
            list1[x] = list1[x].split(' ')
        list1 = self.delNoneElements(list1)
        return list1

    def getCPUinfo(self):
        """
        根据包名，查询CPU使用情况
        :return:
        """
        maxcpu = 0
        cpuinfo = self.exc('adb shell top -n 1| findstr com.zhangyue.iReader.Eink')
        for ci in cpuinfo:
            print 111
            ci = self.getList(ci)
            ci = self.delNoneElements(ci)
            ci.remove(ci[1])
            maxcpu += int(ci[0][2][:-1])
        print maxcpu

    def getPID(self):
        output = self.exc('adb shell ps | findstr com.zhangyue.iReader.Eink')
        output = self.getList(output)
        # output = self.delNoneElements(output)
        lenght = len(output)
        pid = []
        for x in xrange(0, lenght):
            pid.append(output[x][1])
        return pid

    def getFlow(self):
        pid = self.getPID()
        receiveFlow = 0
        transmitFlow = 0
        for x in pid:
            shell = 'adb shell cat /proc/%s/net/dev' % (x)
            output = self.exc(shell)
            output = self.getList(output)
            output = self.delNoneElements(output)
            for x in output:
                if x[0] == 'wlan0:':
                    receiveFlow += int(x[1])
                    transmitFlow += int(x[9])
        return receiveFlow / 1024, transmitFlow / 1024

    def getPower(self):
        output = self.exc('adb shell dumpsys battery')
        output = self.getList(output)
        # output = self.delNoneElements(output)
        power = 0
        for x in output:
            if x[0] == 'level:':
                power = x[1]
        return power


if __name__ == '__main__':
    p = GetValue()
    for x in xrange(0, 1):
        print 'cpuinfo', p.getCPUinfo()
        print 111
        # print 'meminfo', p.getMeminfo()
        # print 'flow', p.getFlow
        # print 'battery', p.getPower
