#! /usr/bin/python3.5
#coding=utf-8

import re
import os
import subprocess
from env import *;
from crash_date import *;
from crash_date_hour import *;
from version import *;
from user import *;
from config import CRASH_SOURCE_PLUGINS;

# 这个类代表一系列stack trace相同的错误信息，是错误统计的基本单位
class Crash:

    def __init__(self, strCrash, strSDKVersion, strRom, strVersionCode, strVersionName, strCrashDate, strCrashDateTime, strUser, fileName):

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

        # 去重之后的崩溃日期信息，%Y-%m-%d形式
        crashDate = CrashDate(strCrashDate);
        self.dictUniqueCrashDates = {crashDate.toString() : crashDate}

        # 去重之后的崩溃日期小时信息，%Y-%m-%d %H-形式
        crashDateHour = CrashDateHour(strCrashDateTime);
        self.dictUniqueCrashDateHours = {crashDateHour.toString() : crashDateHour}

        # 去重之后的用户信息，以i号来识别用户
        user = User(strUser);
        self.dictUniqueUsers = {user.toString() : user}

        # 错误信息的原始字符串
        self.strCrash = strCrash;

        # 错误信息经格式修正后的字符串
        self.strCrashTrimmed = self.trim(self.strCrash);

        # 错误信息经修正后的字符串，写入的文件的路径
        self.fileCrashTrimmed = self.writeTrimmedCrashStr2File(fileName, self.strCrashTrimmed);

        # 本crash属于主工程的crash，还是插件的，是哪个插件的
        self.source = "主工程";
        for crashSource in CRASH_SOURCE_PLUGINS.keys():
            crashSourceKeyWords = CRASH_SOURCE_PLUGINS[crashSource];
            hit = False;
            for keyWord in crashSourceKeyWords:
                if keyWord in self.strCrashTrimmed:
                    hit = True;
                    break;
            if hit:
                self.source = crashSource;
                break;
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

    # 返回dictUniqueVersions
    def getDictUniqueVersions(self):
        return self.dictUniqueVersions;
    pass

    # 加入一条新的崩溃日期信息并去重
    def addCrashDate(self, objNewCrashDate):
        if objNewCrashDate.toString() in self.dictUniqueCrashDates:
            objCrashDate = self.dictUniqueCrashDates[objNewCrashDate.toString()];
            objCrashDate.count = objCrashDate.count + 1;
        else:
            self.dictUniqueCrashDates[objNewCrashDate.toString()] = objNewCrashDate;
    pass

    # 加入一条新的崩溃日期小时信息并去重
    def addCrashDateHour(self, objNewCrashDateHour):
        if objNewCrashDateHour.toString() in self.dictUniqueCrashDateHours:
            objCrashDateHour = self.dictUniqueCrashDateHours[objNewCrashDateHour.toString()];
            objCrashDateHour.count = objCrashDateHour.count + 1;
        else:
            self.dictUniqueCrashDateHours[objNewCrashDateHour.toString()] = objNewCrashDateHour;
    pass

    # 加入一条新的用户信息并去重
    def addUser(self, objNewUser):
        if objNewUser.toString() in self.dictUniqueUsers:
            objUser = self.dictUniqueUsers[objNewUser.toString()];
            objUser.count = objUser.count + 1;
        else:
            self.dictUniqueUsers[objNewUser.toString()] = objNewUser;
    pass

    # 修正错误信息的字符串，把换行符和制表符替换了，再把干扰html的字符替换成html字符，再抹掉一些无关紧要却又影响去重的字符
    def trim(self, untrimmedCrashStr):

        if untrimmedCrashStr.strip() == "":
            return untrimmedCrashStr;
        else:
            trimmedCrashStr = re.sub(r"\\n", "\n", untrimmedCrashStr);
            trimmedCrashStr = re.sub(r"\\t", "\t", trimmedCrashStr);
            # 将&换成&amp;
            trimmedCrashStr = re.sub(r"&", "&amp;", trimmedCrashStr);
            # 将<和>换成&lt;和&gt;
            trimmedCrashStr = re.sub(r"<", "&lt;", trimmedCrashStr);
            trimmedCrashStr = re.sub(r">", "&gt;", trimmedCrashStr);
            # 将"换成&quot;
            trimmedCrashStr = re.sub(r"\"", "&quot;", trimmedCrashStr);
            # 将 obj@hashCFailed to allocate a 86489288 byte allocation with 33554432 free bytes and 82MB until OOMode后面的hashcode换成*，避免影响去重
            trimmedCrashStr = re.sub(r"@[0-9a-z]+", "@*", trimmedCrashStr);
            # 将 appears in /data/data/com.oppo.reader/plugins/pluginwebdiff_bookstore2/1516510781217.apk)中.apk前的数字换成*，避免影响去重
            trimmedCrashStr = re.sub(r"/[0-9]+\.apk\)", "/*.apk", trimmedCrashStr);
            # 将Failed to allocate a xxx byte allocation with xxx free bytes and xxMB until OOM中的数字都替换成*
            trimmedCrashStr = re.sub(r"Failed to allocate a [0-9]+ byte allocation with [0-9]+ free bytes and [0-9]+MB until OOM", "Failed to allocate * byte allocation with * free bytes and *MB until OOM", trimmedCrashStr);
            # 将pid: xxxx替换成pid: *
            trimmedCrashStr = re.sub(r"pid: [0-9]+,", "pid: *,", trimmedCrashStr);
            # 将tid: xxxx替换成tid: *
            trimmedCrashStr = re.sub(r"tid: [0-9]+,", "tid: *,", trimmedCrashStr);
            # 将name: Thread-xxxx 替换成name: Thread-*
            trimmedCrashStr = re.sub(r"name: Thread-[0-9]+ ", "name: Thread-* ", trimmedCrashStr);
            # 将name: GLThread xxxx 替换成name: GLThread *
            trimmedCrashStr = re.sub(r"name: GLThread [0-9]+ ", "name: GLThread * ", trimmedCrashStr);
            # 将com.oppo.reader-x替换成com.oppo.reader-*
            trimmedCrashStr = re.sub(r"com.oppo.reader-[0-9]+", "com.oppo.reader-*", trimmedCrashStr);
            # 将fault addr xxxxxx 替换成fault addr be *
            trimmedCrashStr = re.sub(r"fault addr [0-9a-z]+ ", "fault addr * ", trimmedCrashStr);
            # 将[at 0xxxxx]替换成[at 0x*]
            trimmedCrashStr = re.sub(r"\[at 0x[0-9a-z]+\]", "[at 0x*]", trimmedCrashStr);
            # 将pc xxxxxx替换成pc *
            trimmedCrashStr = re.sub(r"pc [0-9a-z]+ ", "pc * ", trimmedCrashStr);
            # 将Invalid Index x, size is换成Invalid Index *, size is
            trimmedCrashStr = re.sub(r"Invalid index [0-9]+, size is", "Invalid index *, size is", trimmedCrashStr);
            # 紧急情况下，需要把堆栈信息都去掉后再比较，以更好的聚类
            # trimmedCrashStr = re.sub(r"at .*\n", "", trimmedCrashStr)
            # 去掉结尾空格
            trimmedCrashStr = trimmedCrashStr.strip();
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
        # 按比例从高到低排序
        listUniqueVersions = sorted(listUniqueVersions, key=lambda objVersion : objVersion.count, reverse=True);
        for objVersion in listUniqueVersions:
            versionCount = versionCount + objVersion.count;
        strVersionStats = "";
        for objVersion in listUniqueVersions:
            strVersionStats = strVersionStats + "{0},\t{1} of {2},\t{3}%".format(objVersion.toString(), objVersion.count, versionCount, str(round(100.0 * objVersion.count / versionCount)));
            if listUniqueVersions.index(objVersion) != len(listUniqueVersions) - 1:
                strVersionStats = strVersionStats + "\n";
        return strVersionStats;
    pass

    # 打印user统计信息
    def getUserStats(self):
        userCount = 0;
        listUniqueUsers = list(self.dictUniqueUsers.values());
        # 按比例从高到底排序
        listUniqueUsers = sorted(listUniqueUsers, key=lambda objUser : objUser.count, reverse=True);
        for objUser in listUniqueUsers:
            userCount = userCount + objUser.count;
        strUserStats = "";
        for objUser in listUniqueUsers:
            strUserStats = strUserStats + "{0},\t{1} of {2},\t{3}%".format(objUser.toString(), objUser.count, userCount, str(round(100.0 * objUser.count / userCount)));
            if listUniqueUsers.index(objUser) != len(listUniqueUsers) - 1:
                strUserStats = strUserStats + "\n";
        return strUserStats;
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
        listUniqueCrashDates = sorted(listUniqueCrashDates, key=lambda objCrashDate: objCrashDate.toString(), reverse=False);

        for objCrashDate in listUniqueCrashDates:
            crashDateCount = crashDateCount + objCrashDate.count;
        strCrashDateStats = "";
        for objCrashDate in listUniqueCrashDates:
            strCrashDateStats = strCrashDateStats + "{0},\t{1} of {2},\t{3}%".format(objCrashDate.toString(), objCrashDate.count, crashDateCount, str(round(100.0 * objCrashDate.count / crashDateCount)));
            if listUniqueCrashDates.index(objCrashDate) != len(listUniqueCrashDates) - 1:
                strCrashDateStats = strCrashDateStats + "\n";
        return strCrashDateStats;
    pass

    # 打印崩溃日期小时统计信息
    def getCrashDateHourStats(self):
        listUniqueCrashDateHours = list(self.dictUniqueCrashDateHours.values());
        # 按日期小时从小到大排序
        listUniqueCrashDateHours = sorted(listUniqueCrashDateHours, key=lambda objCrashDateHour: objCrashDateHour.toString(), reverse=False);

        if(len(listUniqueCrashDateHours) > 1):
            # 取最小时间
            strMinDateHour = listUniqueCrashDateHours[0].toString();
            # 取最大时间
            strMaxDateHour = listUniqueCrashDateHours[len(listUniqueCrashDateHours) - 1].toString();
        elif(len(listUniqueCrashDateHours) == 1):
            strMinDateHour = strMaxDateHour = listUniqueCrashDateHours[0].toString();

        minDateHour = datetime.datetime.strptime(strMinDateHour, "%Y-%m-%d %H-");
        maxDateHour = datetime.datetime.strptime(strMaxDateHour, "%Y-%m-%d %H-");

        # 把没有崩溃的时段也填充上
        i = minDateHour;
        step = datetime.timedelta(hours=1);

        while i <= maxDateHour:
            iStr = datetime.datetime.strftime(i, "%Y-%m-%d %H-");
            if iStr not in self.dictUniqueCrashDateHours:
                self.dictUniqueCrashDateHours[iStr] = CrashDateHour(iStr, initWithZeroCount=True);
            i = i + step;

        # 再一次按日期小时从小到大排序
        listUniqueCrashDateHours = sorted(self.dictUniqueCrashDateHours.values(), key=lambda objCrashDateHour: objCrashDateHour.toString(), reverse=False);

        strCrashDateHourStats = "";
        for objCrashDateHour in listUniqueCrashDateHours:
            strCrashDateHourStats = strCrashDateHourStats + "{0}, {1}".format(objCrashDateHour.toString(), objCrashDateHour.count);
            if listUniqueCrashDateHours.index(objCrashDateHour) != len(listUniqueCrashDateHours) - 1:
                strCrashDateHourStats = strCrashDateHourStats + "\n";

        return strCrashDateHourStats;
    pass

    # 获取供svg柱状图使用的崩溃日期小时统计信息，需在getCrashDateHourStats方法被调用之后调用
    def getCrashDateHourStatsForHistogram(self):
        # 崩溃的小时时间-崩溃信息的key value pair按崩溃的小时时间，从小到大排序
        listCrashDateHourKVs = sorted(self.dictUniqueCrashDateHours.items(), key=lambda kv: kv[0], reverse=False);
        return listCrashDateHourKVs;
    pass

    # 打印crash比例统计信息
    def getCrashRatioStats(self, totalCrashCount):
        strCrashRatioStats = "------------------crash {0}, {1} of {2}, {3}%------------------------------{4}".format(self.order, self.count, totalCrashCount, str(round(100.0 * self.count / totalCrashCount)), self.source);
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
    def getRetracedCrashMessage(self, strMainProjectMappingFilePath, strTuplePluginMappingFilePath):
        fileCrashTrimmedAbsPath = os.path.abspath(self.fileCrashTrimmed.name);
        commands = ["retrace", os.path.abspath(strMainProjectMappingFilePath), fileCrashTrimmedAbsPath];
        byteResult = subprocess.check_output(commands);
        strResult = byteResult.decode();

        with open(fileCrashTrimmedAbsPath, "w") as f:
            f.write(strResult);
            f.close();

        for strPluginMappingFilePath in strTuplePluginMappingFilePath:
            commands = ["retrace", os.path.abspath(strPluginMappingFilePath), fileCrashTrimmedAbsPath];
            byteResult = subprocess.check_output(commands)
            strResult = byteResult.decode();
            with open(fileCrashTrimmedAbsPath, "w") as f:
                f.write(strResult);
                f.close();

        # retrace程序会把换行和制表符又替换回字面的"\n"和"\t"，所以这里要再替换回来
        strResult = re.sub(r"\\n", "\n", strResult);
        strResult = re.sub(r"\\t", "\t", strResult);
        return strResult;
    pass


    # 在去重时，dict所使用的key应为strCrashTrimmed去掉所有行号(xx:yyyyy)之后的字符串
    def getKey(self):
        return re.sub(r"\([a-zA-Z0-9\.]+:[0-9]*\)", "", self.strCrashTrimmed);
    pass