#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表由相同的来源引起的一类crash的数量统计，＂来源＂指来自主工程，还是哪个插件
class CrashSameSource:

    def __init__(self, strSource, strListSourceKeywords):

        # source的字符串,　表示来自主工程，还是哪个插件
        self.strSource = strSource;

        # 符合这个source的crash，其crashMsg中必须包含如下列表中的关键字
        self.strListSourceKeywords = strListSourceKeywords;

        # 这个source的crash包含多少种，这个数量等于crash对象的数量
        self.crashTypeCount = 0;

        # 这个source的crash包含多少条
        self.crashTimeCount = 0;

    pass;

    def toString(self, numTotalCrashes):
        crashTimePercentage = round(100.0 * self.crashTimeCount / numTotalCrashes);
        return self.strSource + " : " + str(self.crashTimeCount) + " (" + str(crashTimePercentage) + "%)" + "(" + str(self.crashTypeCount) + "types)"
    pass;
