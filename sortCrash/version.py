#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表一种app版本，包括versionCode和versionName
class Version:

    def __init__(self, strVersionCode, strVersionName):

        # 在某条去重后的错误中的出现次数
        self.count = 1;

        # versionCode
        self.strVersionCode = strVersionCode;

        # versionName
        self.strVersionName = strVersionName;
    pass

    def toString(self):
        if str(self.strVersionCode).strip() == "" and str(self.strVersionName).strip() == "":
            return "unknown version";
        else:
            return str(self.strVersionCode) + ", " + str(self.strVersionName);
    pass
