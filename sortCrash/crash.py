#! /usr/bin/python3.5
#coding=utf-8

import re
import os
import subprocess
from env import *;
from crashdate import *;
from version import *;

# 这个类代表一系列stack trace相同的错误信息，是错误统计的基本单位
class Crash:

    def __init__(self, strCrash, strSDKVersion, strRom, strVersionCode, strVersionName, strCrashDate, fileName):

        # crash序号
        self.order = 0;

        # 错误信息的出现次数
        self.count = 1;

        # 去重之后的运行环境信息，内含android version和rom信息
        env = Env(strSDKVersion, strRom);
        self.dictUniqueEnvs = {env.toString() : env};

        # 去重之后的软件版本信息，内含versionCode和versionName信息
        version = Version(strVersionCode, strVersionName);
        self.dictUniqueVersions = {version.toString() : version};

        # 去重之后的崩溃日期信息，yyyy-mm-dd形式
        crashDate = CrashDate(strCrashDate);
        self.dictUniqueCrashDates = {crashDate.toString() : crashDate}

        # 错误信息的原始字符串
        self.strCrash = strCrash;

        # 错误信息经格式修正后的字符串
        self.strCrashTrimmed = self.trim(self.strCrash);

        # 错误信息经修正后的字符串，写入的文件的路径
        self.fileCrashTrimmed = self.writeTrimmedCrashStr2File(fileName, self.strCrashTrimmed);

    pass


    # 加入一条新的env信息并去重
    def addEnv(self, objNewEnv):

        if objNewEnv.toString() in self.dictUniqueEnvs:
            objEnv = self.dictUniqueEnvs[objNewEnv.toString()];
            objEnv.count = objEnv.count + 1;
        else:
            self.dictUniqueEnvs[objNewEnv.toString()] = objNewEnv;
    pass


    # 加入一条新的version信息并去重
    def addVersion(self, objNewVersion):

        if objNewVersion.toString() in self.dictUniqueVersions:
            objVersion = self.dictUniqueVersions[objNewVersion.toString()];
            objVersion.count = objVersion.count + 1;
        else:
            self.dictUniqueVersions[objNewVersion.toString()] = objNewVersion;
    pass


    # 加入一条新的崩溃日期信息并去重
    def addCrashDate(self, objNewCrashDate):

        if objNewCrashDate.toString() in self.dictUniqueCrashDates:
            objCrashDate = self.dictUniqueCrashDates[objNewCrashDate.toString()];
            objCrashDate.count = objCrashDate.count + 1;
        else:
            self.dictUniqueCrashDates[objNewCrashDate.toString()] = objNewCrashDate;
    pass


    # 修正错误信息的字符串，把换行符和制表符替换了，再抹掉一些无关紧要却又影响去重的字符
    def trim(self, untrimmedCrashStr):

        if untrimmedCrashStr.strip() == "":
            return untrimmedCrashStr;
        else:
            # untrimmedCrashStr = untrimmedCrashStr.replace("\\n", "\n").replace("\\t", "\t");
            trimmedCrashStr = re.sub(r"\\n", "\n", untrimmedCrashStr);
            trimmedCrashStr = re.sub(r"\\t", "\t", trimmedCrashStr);
            # 将 obj@hashCFailed to allocate a 86489288 byte allocation with 33554432 free bytes and 82MB until OOMode后面的hashcode换成*，避免影响去重
            trimmedCrashStr = re.sub(r"@[0-9a-z]+", "@*", trimmedCrashStr);
            # 将 appears in /data/data/com.oppo.reader/plugins/pluginwebdiff_bookstore2/1516510781217.apk)中.apk前的数字换成*，避免影响去重
            trimmedCrashStr = re.sub(r"/[0-9]+\.apk\)", "/*.apk", trimmedCrashStr);
            # 将Failed to allocate a xxx byte allocation with xxx free bytes and xxMB until OOM中的数字都替换成*
            trimmedCrashStr = re.sub(r"Failed to allocate a [0-9]+ byte allocation with [0-9]+ free bytes and [0-9]+MB until OOM", "Failed to allocate * byte allocation with * free bytes and *MB until OOM", trimmedCrashStr);
            return trimmedCrashStr;
    pass


    # 错误信息的字符串写入文件
    def writeTrimmedCrashStr2File(self, fileName, content):
        fileCrashTrimmed = open(fileName, 'w');
        fileCrashTrimmed.write(content);
        fileCrashTrimmed.close();
        return fileCrashTrimmed;
    pass


    # 打印env统计信息
    def getEnvStats(self):
        envCount = 0;
        listUniqueEnvs = list(self.dictUniqueEnvs.values());
        # 按比例从高到低排序
        listUniqueEnvs = sorted(listUniqueEnvs, key=lambda objEnv : objEnv.count, reverse=True);
        for objEnv in listUniqueEnvs:
            envCount = envCount + objEnv.count;
        strEnvStats = "";
        for objEnv in listUniqueEnvs:
            strEnvStats = strEnvStats + "{0},\t{1} of {2},\t{3}%".format(objEnv.toString(), objEnv.count, envCount, str(round(100.0 * objEnv.count / envCount)));
            if listUniqueEnvs.index(objEnv) != len(listUniqueEnvs) - 1:
                strEnvStats = strEnvStats + "\n";
        return strEnvStats;
    pass


    # 打印version统计信息
    def getVersionStats(self):
        versionCount = 0;
        listUniqueVersions = list(self.dictUniqueVersions.values());
        for objVersion in listUniqueVersions:
            versionCount = versionCount + objVersion.count;
        strVersionStats = "";
        for objVersion in listUniqueVersions:
            strVersionStats = strVersionStats + "{0},\t{1} of {2},\t{3}%".format(objVersion.toString(), objVersion.count, versionCount, str(round(100.0 * objVersion.count / versionCount)));
            if listUniqueVersions.index(objVersion) != len(listUniqueVersions) - 1:
                strVersionStats = strVersionStats + "\n";
        return strVersionStats;
    pass

    # 打印versionNames
    def getVersionNamesSet(self):
        return self.dictUniqueVersions.keys();
    pass

    # 打印崩溃日期统计信息
    def getCrashDateStats(self):
        crashDateCount = 0;
        listUniqueCrashDates = list(self.dictUniqueCrashDates.values());
        # 按日期从小到大排序
        listUniqueCrashDates = sorted(listUniqueCrashDates, key=lambda objCrashDate: objCrashDate.strCrashDate, reverse=False);

        for objCrashDate in listUniqueCrashDates:
            crashDateCount = crashDateCount + objCrashDate.count;
        strCrashDateStats = "";
        for objCrashDate in listUniqueCrashDates:
            strCrashDateStats = strCrashDateStats + "{0},\t{1} of {2},\t{3}%".format(objCrashDate.toString(), objCrashDate.count, crashDateCount, str(round(100.0 * objCrashDate.count / crashDateCount)));
            if listUniqueCrashDates.index(objCrashDate) != len(listUniqueCrashDates) - 1:
                strCrashDateStats = strCrashDateStats + "\n";
        return strCrashDateStats;
    pass


    # 打印crash比例统计信息
    def getCrashRatioStats(self, totalCrashCount):
        strCrashRatioStats = "------------------crash {0}, {1} of {2}, {3}%------------------------------".format(self.order, self.count, totalCrashCount, str(round(100.0 * self.count / totalCrashCount)));
        return strCrashRatioStats;
    pass

    # 打印crash比例，只显示百分比
    def getCrashRatioPercentageOnly(self, totalCrashCount):
        return str(round(100.0 * self.count / totalCrashCount)) + "%";
    pass

    # 打印未经retrace的crash内容
    def getUnRetracedCrashMessage(self):
        with open(self.fileCrashTrimmed.name, "r") as f:
            return f.read();
    pass

    # 打印经retrace后的crash内容
    def getRetracedCrashMessage(self, strMappingFilePath):
        commands = ["retrace", os.path.abspath(strMappingFilePath), os.path.abspath(self.fileCrashTrimmed.name)];
        byteResult = subprocess.check_output(commands);
        strResult = byteResult.decode();
        # retrace程序会把换行和制表符又替换回字面的"\n"和"\t"，所以这里要再替换回来
        strResult = re.sub(r"\\n", "\n", strResult);
        strResult = re.sub(r"\\t", "\t", strResult);
        return strResult;
    pass


    # 在去重时，dict所使用的key应为strCrashTrimmed去掉所有行号(xx:yyyyy)之后的字符串
    def getKey(self):
        return re.sub(r"\([a-zA-Z0-9\.]+:[0-9]*\)", "", self.strCrashTrimmed);
    pass