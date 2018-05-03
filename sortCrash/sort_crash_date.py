#! /usr/bin/python3.5
#coding=utf-8

from config import *;
import xlrd;
import xlwt;
import progressbar;
import datetime;

# 获取一定范围内的所有日期，输入参数为yyyyMMdd形式
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

# 生成只包含指定日期崩溃的excel表，返回新表的路径
# strDateRange的形式是:
# 空 不指定日期，则返回的是原来表的路径
# yyyyMMdd 指定一天
# yyyyMMdd-yyyyMMdd 指定一段日期，起始日期和结束日期都包括在内
def generateExcelForCrashHappeningAtSpecificDays(strXlsPath, *args):

    # 检查指定的日期参数的合法性
    # 未传入要筛选的日期，直接返回原路径
    if len(args) == 0:
        return strXlsPath;
    elif len(args) == 1:
        strDateSelection = str(args[0]);
        if "-" in strDateSelection:
            startDate = strDateSelection.split("-")[0];
            endDate = strDateSelection.split("-")[1];
        else:
            startDate = strDateSelection;
            endDate = strDateSelection;

    dates = dateRange(startDate, endDate);

    # excel工作库
    xlsFile = xlrd.open_workbook(strXlsPath);

    # 工作库的目录
    strXlsDirPath = os.path.split(strXlsPath)[0];

    # 工作库的文件名（去掉后缀）
    strXlsName = os.path.splitext(os.path.split(strXlsPath)[1])[0];

    # excel工作表
    xlsSheet = xlsFile.sheets()[0];

    # 提取崩溃日期列
    listStrRowCrashDates = xlsSheet.col_values(EXCEL_COL_INDEX_CRASH_DATETIME);

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

    # 写入新的库里的表
    bar = progressbar.ProgressBar();
    j = 0;

    for i in bar(range(len(listStrRowCrashTimes))):
        # 检测日期是否在选定的日期范围内
        time = datetime.datetime.strptime(listStrRowCrashTimes[i], "%Y-%m-%d %H:%M:%S");
        strDate = str(time.date());
        if strDate in dates:
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_ANDROID_VERSION, listStrRowAndroidVersions[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_PACKAGE_NAME, listStrRowPackageNames[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_CHANNEL_ID, listStrRowChannelIDs[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_ROM, listStrRowRoms[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_VERSION_CODE, listStrRowVersionCodes[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_LCDTYPE, listStrRowLCDTypes[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_CLIENT_SOURCE, listStrRowClientSources[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_CRASH, listStrRowCrashes[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_VERSION_NAME, listStrRowVersionNames[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_PHONE_MODEL, listStrRowPhoneModels[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_ID, listStrRowIDs[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_CRASH_DATETIME, listStrRowCrashTimes[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_I_ACCOUNT, listStrRowIAccounts[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_SCREENISH, listStrRowScreenishes[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_OTHER_MSG, listStrRowOtherMsgs[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_INTERNAL_APP_VERSION, listStrRowInternalAppVersions[i]);
            rsltXlsSheet.write(j, EXCEL_COL_INDEX_UPLOAD_TIME, listStrRowUploadTimes[i]);
            j = j + 1;

    # 按新的名字保存新表
    strNewPath = os.path.join(strXlsDirPath, strXlsName + "_" + args[0] + ".xls");

    rsltXlsFile.save(strNewPath);

    return strNewPath;

pass

# 必须有一个或两个输入参数
if len(sys.argv) == 2:
    generateExcelForCrashHappeningAtSpecificDays(sys.argv[1]);
elif len(sys.argv) == 3:
    generateExcelForCrashHappeningAtSpecificDays(sys.argv[1], sys.argv[2]);
