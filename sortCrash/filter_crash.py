#! /usr/bin/python3.5
#coding=utf-8

from config import *;
import xlrd;
import xlwt;
import progressbar;
import datetime;
import random;

#------------------------崩溃信息过滤-------------------------------
# 需要过滤掉的崩溃信息，包含下面字符串的就算
EXCLUDE_MSGS = (
    # 自主抛出的异常，不会导致崩溃
    "DEBUGt_CRASH",
    "android.content.res.Resources$NotFoundException",
);

#------------------------崩溃日期过滤--------------------------------
# 需要过滤掉的日期，此日期前的(不包括这一天)都被过滤掉，日期形式yyyyMMdd
EXCLUDE_DATE_BEFORE = ""
EXCLUDE_DATE_BEFORE = "20180718";
# 需要过滤掉的日期，此日期后的(不包括这一天)都被过滤掉，日期形式yyyyMMdd
EXCLUDE_DATE_AFTER = ""
EXCLUDE_DATE_AFTER = "20180718";

#-----------------------版本名过滤------------------------------------
# 除此之外的版本名会被过滤掉，不写为不过滤
INCLUDE_VERSION_NAMES = ();
# 形式：x.x.x.yyyyMMdd
INCLUDE_VERSION_NAMES = ("6.2.1.20180613",);
# INCLUDE_VERSION_NAMES = ("6.1.9.20180202","6.1.9.20180307",);

#-----------------------同一用户同一时间（指年月日时分秒都一样）的多条崩溃，只取其中一条-------------------
# 是否开启这个功能
IS_FILTERING_CLUSTER_CRASHES = False;

# 获取一定范围内的所有日期，输入参数为yyyyMMdd形式
# 返回的是date对象的列表
def dateRange(beginDate, endDate):

    beginDate = datetime.datetime.strptime(beginDate, "%Y%m%d");
    endDate = datetime.datetime.strptime(endDate, "%Y%m%d");
    i = beginDate;
    step = datetime.timedelta(days=1);
    dates = [];

    while i <= endDate:
        dates.append(str(i.date()));
        i = i + step;

    return dates
pass

# 按各种条件过滤excel表，生成过滤后的新表，并返回新表的路径
def filterCrash(strXlsPath):

    # excel工作库
    xlsFile = xlrd.open_workbook(strXlsPath);

    # 工作库的目录
    strXlsDirPath = os.path.split(strXlsPath)[0];

    # 工作库的文件名（去掉后缀）
    strXlsName = os.path.splitext(os.path.split(strXlsPath)[1])[0];

    # excel工作表
    xlsSheet = xlsFile.sheets()[0];

    # 新的只包含指定日期崩溃的excel库
    rsltXlsFile = xlwt.Workbook(encoding = 'utf-8')

    # 新的库里加个表
    rsltXlsSheet = rsltXlsFile.add_sheet("返回结果", cell_overwrite_ok=True);

    # 提取各列信息
    listStrRowAndroidVersions = xlsSheet.col_values(EXCEL_COL_INDEX_ANDROID_VERSION);
    listStrRowPackageNames = xlsSheet.col_values(EXCEL_COL_INDEX_PACKAGE_NAME);
    listStrRowChannelIDs = xlsSheet.col_values(EXCEL_COL_INDEX_CHANNEL_ID);
    listStrRowRoms = xlsSheet.col_values(EXCEL_COL_INDEX_ROM);
    listStrRowVersionCodes = xlsSheet.col_values(EXCEL_COL_INDEX_VERSION_CODE);
    listStrRowLCDTypes = xlsSheet.col_values(EXCEL_COL_INDEX_LCDTYPE);
    listStrRowClientSources = xlsSheet.col_values(EXCEL_COL_INDEX_CLIENT_SOURCE);
    listStrRowCrashes = xlsSheet.col_values(EXCEL_COL_INDEX_CRASH);
    listStrRowVersionNames = xlsSheet.col_values(EXCEL_COL_INDEX_VERSION_NAME);
    listStrRowPhoneModels = xlsSheet.col_values(EXCEL_COL_INDEX_PHONE_MODEL);
    listStrRowIDs = xlsSheet.col_values(EXCEL_COL_INDEX_ID);
    listStrRowCrashTimes = xlsSheet.col_values(EXCEL_COL_INDEX_CRASH_DATETIME);
    listStrRowIAccounts = xlsSheet.col_values(EXCEL_COL_INDEX_I_ACCOUNT);
    listStrRowScreenishes = xlsSheet.col_values(EXCEL_COL_INDEX_SCREENISH);
    listStrRowOtherMsgs = xlsSheet.col_values(EXCEL_COL_INDEX_OTHER_MSG);
    listStrRowInternalAppVersions = xlsSheet.col_values(EXCEL_COL_INDEX_INTERNAL_APP_VERSION);
    listStrRowUploadTimes = xlsSheet.col_values(EXCEL_COL_INDEX_UPLOAD_TIME);

    # 同一用户同一时间的崩溃只取其中一条，不同时间相差一秒的也只取一条
    dictUniqueIAccountToCrashTimes = {};

    # 写入新的库里的表
    bar = progressbar.ProgressBar();

    dstLine = 0;
    for i in bar(range(len(listStrRowCrashes))):

        # 提取崩溃列
        strCrash = listStrRowCrashes[i];
        skip = False;

        # 看看有没有要被过滤的crash msg
        for EXCLUDE_MSG in EXCLUDE_MSGS:
            # crash msg中要被过滤掉的
            if EXCLUDE_MSG in strCrash:
                skip = True;
                break;

        # 看看有没有要被过滤掉的日期
        if EXCLUDE_DATE_BEFORE.strip() != "" and EXCLUDE_DATE_AFTER.strip() != "":
            includeDates = dateRange(EXCLUDE_DATE_BEFORE.strip(), EXCLUDE_DATE_AFTER.strip());
            # 表中的日期有可能格式不对，要try except
            try:
                crashDate = str(datetime.datetime.strptime(listStrRowCrashTimes[i], "%Y-%m-%d %H:%M:%S").date());
            except BaseException:
                print("problematic date format : " + listStrRowCrashTimes[i] + " @row " + str(i) + ", skip");
                skip = True

            if crashDate not in includeDates:
                skip = True;

        # versionName为空的过滤掉
        if listStrRowVersionNames[i].strip() == "" or listStrRowVersionCodes[i] == "":
            skip = True

        # versionName不在规定范围的过滤掉
        if len(INCLUDE_VERSION_NAMES) >=1 and listStrRowVersionNames[i] not in INCLUDE_VERSION_NAMES:
            skip = True;

        if IS_FILTERING_CLUSTER_CRASHES:
            # 同一用户同一时间的崩溃，如果已经有了，则后来的都被过滤掉
            # 同一用户不同时间的崩溃，如果相差一秒，则也被过滤掉
            # 注意，如果i号为空，则要将i号的位置赋予一个随机数，因为空i号可能代表任何用户，不能视作同一个用户
            if listStrRowIAccounts[i].strip() == "":
                keyIAccount = str(random.randint(0,100000000));
            else:
                keyIAccount = listStrRowIAccounts[i];

            if keyIAccount in dictUniqueIAccountToCrashTimes:
                # 上一秒的时间字符串
                strPrevSecond = datetime.datetime.strftime(datetime.datetime.strptime(listStrRowCrashTimes[i], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(seconds=1), "%Y-%m-%d %H:%M:%S");
                # 这一秒的时间字符串
                strCurSecond = listStrRowCrashTimes[i];
                # 下一秒的时间字符串
                strNextSecond = datetime.datetime.strftime(datetime.datetime.strptime(listStrRowCrashTimes[i], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1), "%Y-%m-%d %H:%M:%S");

                # 这个i号的所有崩溃时间
                strListCrashTimesOfThisIAccount = dictUniqueIAccountToCrashTimes[keyIAccount];

                # 如果这次崩溃的时间，及其上一秒和下一秒和这个用户出现的其它崩溃的时间一样，则过滤掉
                if strPrevSecond in strListCrashTimesOfThisIAccount or strCurSecond in strListCrashTimesOfThisIAccount or strNextSecond in strListCrashTimesOfThisIAccount:
                    skip = True;

                # 这次崩溃的时间加入这个用户的崩溃时间表中
                strListCrashTimesOfThisIAccount.append(strCurSecond);
                dictUniqueIAccountToCrashTimes[keyIAccount] = strListCrashTimesOfThisIAccount;
            else:
                dictUniqueIAccountToCrashTimes[keyIAccount] = [listStrRowCrashTimes[i], ];

        # 同一用户在某次这次崩溃的上一秒也崩溃过，则本次崩溃被过滤掉

        # 任何一条件导致该条被过滤，则不写入该条到新的excel文件
        if skip:
            continue;

        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_ANDROID_VERSION, listStrRowAndroidVersions[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_PACKAGE_NAME, listStrRowPackageNames[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_CHANNEL_ID, listStrRowChannelIDs[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_ROM, listStrRowRoms[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_VERSION_CODE, listStrRowVersionCodes[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_LCDTYPE, listStrRowLCDTypes[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_CLIENT_SOURCE, listStrRowClientSources[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_CRASH, listStrRowCrashes[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_VERSION_NAME, listStrRowVersionNames[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_PHONE_MODEL, listStrRowPhoneModels[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_ID, listStrRowIDs[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_CRASH_DATETIME, listStrRowCrashTimes[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_I_ACCOUNT, listStrRowIAccounts[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_SCREENISH, listStrRowScreenishes[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_OTHER_MSG, listStrRowOtherMsgs[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_INTERNAL_APP_VERSION, listStrRowInternalAppVersions[i]);
        rsltXlsSheet.write(dstLine, EXCEL_COL_INDEX_UPLOAD_TIME, listStrRowUploadTimes[i]);
        dstLine = dstLine + 1;

    # 按新的名字保存新表
    strNewPath = os.path.join(strXlsDirPath, strXlsName + "_filtered.xls");

    rsltXlsFile.save(strNewPath);

    return strNewPath;

pass

# 必须输入一个参数，即原始excel表的路径
if len(sys.argv) == 2:
    filterCrash(sys.argv[1]);
