#! /usr/bin/python3.5
#coding=utf-8

import xlrd
import shutil
import progressbar
from crash import *
from crash_same_cause import *
from web import *

# 关注哪些cause进行分类统计
SAME_CAUSE_LIST = [
    CrashSameCause("com.zhangyue.common.xeonPush.services.ReaderJobService"),
    CrashSameCause("java.lang.ClassNotFoundException"),
    CrashSameCause("java.lang.NoClassDefFoundError"),
    CrashSameCause("java.lang.IndexOutOfBoundsException: Invalid index"),
];
# 不关注的都归类到others
OTHER_CAUSE = CrashSameCause();

# 打印出去重和retrace之后的崩溃信息，mappingFile是可选参数，如果不传，则不进行retrace
def sortCrashes(strXlsPath, *args):

    # excel工作库
    xlsFile = xlrd.open_workbook(strXlsPath);

    # excel工作表
    xlsSheet = xlsFile.sheets()[0];

    # 提取各列的信息
    listStrRowCrashes = xlsSheet.col_values(EXCEL_COL_INDEX_CRASH);
    listStrRowAndroidVersions = xlsSheet.col_values(EXCEL_COL_INDEX_ANDROID_VERSION);
    listStrRowRoms = xlsSheet.col_values(EXCEL_COL_INDEX_ROM);
    listStrRowVersionCodes = xlsSheet.col_values(EXCEL_COL_INDEX_VERSION_CODE);
    listStrRowVersionNames = xlsSheet.col_values(EXCEL_COL_INDEX_VERSION_NAME);
    listStrRowCrashDateTimes = xlsSheet.col_values(EXCEL_COL_INDEX_CRASH_DATETIME);
    listStrRowUsers = xlsSheet.col_values(EXCEL_COL_INDEX_I_ACCOUNT);
    listStrRowCrashDates = [];

    # 提取崩溃日期
    for i in range(len(listStrRowCrashDateTimes)):
        try:
            parsedDateTime = datetime.datetime.strptime(listStrRowCrashDateTimes[i], "%Y-%m-%d %H:%M:%S");
        except BaseException:
            # 对于格式错误的日期，用1970-01-01 00:00:00代替，以保证后续流程正确性，无法直接删掉错误数据，会影响数据个数
            listStrRowCrashDateTimes[i] = "1970-01-01 00:00:00"
            parsedDateTime = datetime.datetime.strptime(listStrRowCrashDateTimes[i], "%Y-%m-%d %H:%M:%S");
        listStrRowCrashDates.append(datetime.datetime.strftime(parsedDateTime, "%Y-%m-%d"));

    # 存储崩溃信息的临时文件
    if not os.path.isdir(OUTPUT_TMP_DIR_PATH):
        os.mkdir(OUTPUT_TMP_DIR_PATH);

    # 去重的dict
    dictUniqueCrashes = {};

    # 有多少条崩溃记录
    totalCrashes = 0;

    # 去重过程
    for i in range(len(listStrRowCrashes)):

        # 获取excel中每一条崩溃信息
        strRowCrash = listStrRowCrashes[i];
        totalCrashes = totalCrashes + 1;

        # 获取excel中每一条android version信息
        strAndroidVersion = listStrRowAndroidVersions[i];

        # 获取excel中每一条rom信息
        strRom = listStrRowRoms[i];

        # 获取excel中每一条的versionCode信息
        strVersionCode = listStrRowVersionCodes[i];

        # 获取excel中每一条的versionName信息
        strVersionName = listStrRowVersionNames[i];

        # 获取excel中每一条崩溃日期信息
        strCrashDate = listStrRowCrashDates[i];

        # 获取excel中每一条崩溃日期+时间信息
        strCrashDateTime = listStrRowCrashDateTimes[i];

        # 获取excel中每一条用户信息
        strUser = listStrRowUsers[i];
        # 如果为空，即未统计到i号，将它设置为"unknown user"
        if strUser.strip() == "":
            strUser = "unknown user";

        # 建立crash对象
        objCrash = Crash(strRowCrash, strAndroidVersion, strRom, strVersionCode, strVersionName, strCrashDate, strCrashDateTime, strUser,
                         OUTPUT_TMP_DIR_PATH + "/crashFile_" + str(i) + ".txt");

        # 出现过此种错误，数量+1，新增env信息
        if objCrash.getKey() in dictUniqueCrashes:
            objValueCrash = dictUniqueCrashes[objCrash.getKey()];
            objValueCrash.count = objValueCrash.count + 1;
            objValueCrash.addEnv(Env(strAndroidVersion, strRom));
            objValueCrash.addVersion(Version(strVersionCode, strVersionName));
            objValueCrash.addCrashDate(CrashDate(strCrashDate));
            objValueCrash.addCrashDateHour(CrashDateHour(strCrashDateTime));
            objValueCrash.addUser(User(strUser));
        # 没出现过此种错误，加入字典
        else:
            dictUniqueCrashes[objCrash.getKey()] = objCrash;

    # 按比例从高到底排序
    listUniqueCrashesKV = sorted(dictUniqueCrashes.items(),
                                 key=lambda kv: kv[1].count, reverse=True)

    # 排序后写入序号
    order = 1;
    for (keyCrash, objCrash) in listUniqueCrashesKV:
        objCrash.order = order;
        order = order + 1;

    # 运行shell脚本retrace，反混淆崩溃信息
    # 打印unique crash的宏观统计信息到html
    webOutput = WebOutput(strXlsPath);

    bar = progressbar.ProgressBar();
    print("working on it:");

    for i in bar(range(len(listUniqueCrashesKV))):

        uniqueCrashKV = listUniqueCrashesKV[i];

        keyCrash = uniqueCrashKV[0];
        objCrash = uniqueCrashKV[1];

        isInSameCauseList = False;
        # 统计本crash是否符合关注的same cause
        for crashSameCause in SAME_CAUSE_LIST:
            # 某个crash属于我们关注的某个same cause
            if crashSameCause.strCause in objCrash.strCrash:
                crashSameCause.crashTypeCount = crashSameCause.crashTypeCount + 1;
                crashSameCause.crashTimeCount = crashSameCause.crashTimeCount + objCrash.count;
                isInSameCauseList = True;
                break;

        # 不在的话属于其它类的cause
        if not isInSameCauseList:
            OTHER_CAUSE.crashTypeCount = OTHER_CAUSE.crashTypeCount + 1;
            OTHER_CAUSE.crashTimeCount = OTHER_CAUSE.crashTimeCount + objCrash.count;

        webOutput.beginCurCrash(str(objCrash.order), objCrash.getCrashRatioPercentageOnly(totalCrashes));

        webOutput.writeCrashRatioStats(objCrash.getCrashRatioStats(totalCrashes), str(objCrash.order));
        webOutput.writeEnvStats(objCrash.getEnvStats(), str(objCrash.order));
        webOutput.writeVersionStats(objCrash.getVersionStats(), objCrash.getVersionNamesSet(), str(objCrash.order), objCrash.getDictUniqueVersions());
        webOutput.writeUserStats(objCrash.getUserStats(), str(objCrash.order));
        webOutput.writeCrashDateStats(objCrash.getCrashDateStats(), str(objCrash.order));
        # 可以输出柱状图了，就不输出文字版的小时崩溃信息了
        # webOutput.writeCrashDateHourStats(objCrash.getCrashDateHourStats(), str(objCrash.order));
        # 必须调一下getCrashDateHourStats方法以准备好数据
        objCrash.getCrashDateHourStats();
        webOutput.writeCrashDateHourSvgHistogram(objCrash.getCrashDateHourStatsForHistogram(), str(objCrash.order));

        # 打印crash内容
        # 未提供mappingFile，不进行retrace，直接打印每个错误文件中的内容
        if len(args) == 0:
            webOutput.writeCrashMessage(objCrash.getUnRetracedCrashMessage(), str(objCrash.order));
        # 提供了mappingFile，即args[0]，打印retrace后的结果
        else:
            webOutput.writeCrashMessage(objCrash.getRetracedCrashMessage(args[0]), str(objCrash.order));

    # 打印到浏览器
    # 确定html输出路径，与输入的excel一样名字和路径
    strHtmlDir = os.path.split(strXlsPath)[0];
    strHtmlName = os.path.splitext(os.path.split(strXlsPath)[1])[0];
    strHtmlExt = "html";
    strHtmlOutputAbsPath = strHtmlDir + os.sep + strHtmlName + "." + strHtmlExt;
    webOutput.printToBrowser(strHtmlOutputAbsPath, totalCrashes, SAME_CAUSE_LIST, OTHER_CAUSE);

    # 清除临时文件夹
    shutil.rmtree(OUTPUT_TMP_DIR_PATH);
    print("done.");
pass

# 无输入参数，使用test.xls
if len(sys.argv) == 1:

    sortCrashes(INPUT_TEST_XLS_PATH);
# 无retrace
elif len(sys.argv) == 2:
    sortCrashes(sys.argv[1]);
# 有retrace
elif len(sys.argv) == 3:
    sortCrashes(sys.argv[1], sys.argv[2]);
