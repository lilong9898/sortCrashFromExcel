#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表一种崩溃日期
class CrashDate:

    def __init__(self, strCrashDate):

        # 在某条去重后的错误中的出现次数
        self.count = 1;

        # 崩溃日期字符串%Y-%m-%d形式
        self.strCrashDate = strCrashDate;
        pass;


    def toString(self):
        return self.strCrashDate;