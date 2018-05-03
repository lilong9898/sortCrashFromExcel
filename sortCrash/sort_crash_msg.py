#! /usr/bin/python3.5
#coding=utf-8

from config import *;
import xlrd;
import xlwt;
import progressbar;
import datetime;

# 生成不包含指定commit msg的excel表，返回新表的路径
def generateExcelForCrashExcludingSpecificCrashMsgs(strXlsPath, *args):

    # 检查指定的日期参数的合法性
    # 未传入要筛选的日期，直接返回原路径
    if len(args) == 0:
        return strXlsPath;
    elif len(args) == 1:
        strExcludingMsg = str(args[0]);

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

    for i in bar(range(len(listStrRowCrashes))):
        strCrash = listStrRowCrashes[i];
        if strExcludingMsg not in strCrash:
            if j == 1:
                print(strExcludingMsg + ":" + strCrash)
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
    generateExcelForCrashExcludingSpecificCrashMsgs(sys.argv[1]);
elif len(sys.argv) == 3:
    generateExcelForCrashExcludingSpecificCrashMsgs(sys.argv[1], sys.argv[2]);
