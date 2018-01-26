#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表一种运行环境，包括android版本和机型
class Env:

    def __init__(self, strAndroidVersion, strRom):

        # 在某条去重后的错误中的出现次数
        self.count = 1;

        # android版本
        self.strAndroidVersion = strAndroidVersion;

        # 机型
        self.strRom = strRom;
        pass;


    def toString(self):
        return str(self.strAndroidVersion) + ", " + str(self.strRom);