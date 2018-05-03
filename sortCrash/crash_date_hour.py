#! /usr/bin/python3.5
#coding=utf-8

import datetime

# 这个类代表某个日期的某个整点到下个整点的时段
class CrashDateHour:

    # 构造参数形式 %Y-%m-%d %H:%M:%S
    def __init__(self, strCrashDateTime, initWithZeroCount = False):

        # 在某条去重后的错误中的出现次数
        if initWithZeroCount:
            self.count = 0;
            self.strDateHour = strCrashDateTime;
        else:
            self.count = 1;
            # %Y-%m-%d %H-形式的字符串
            self.strDateHour = datetime.datetime.strftime(datetime.datetime.strptime(strCrashDateTime, "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H-");


    pass

    def toString(self):
        return self.strDateHour;
    pass
