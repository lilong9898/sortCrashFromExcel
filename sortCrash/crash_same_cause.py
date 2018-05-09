#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表由相同原因引起的一类crash的数量统计，"相同原因"看crash msg中是否包含同样的cause字符串
class CrashSameCause:

    def __init__(self, strCause = "others"):

        # cause的字符串，凡是crash msg中包含这个cause字符串的，就属于same cause，会对应到本类的一个实例，并更新这个实例中的数据
        self.strCause = strCause;

        # 这个cause的crash包含多少种，这个数量等于crash对象的数量
        self.crashTypeCount = 0;

        # 这个cause的crash包含多少条
        self.crashTimeCount = 0;

    pass;

    def toString(self, numTotalCrashes):
        crashTimePercentage = round(100.0 * self.crashTimeCount / numTotalCrashes);
        return self.strCause + " : " + str(self.crashTimeCount) + " (" + str(crashTimePercentage) + "%)" + "(" + str(self.crashTypeCount) + "types)"
    pass;

pass;
