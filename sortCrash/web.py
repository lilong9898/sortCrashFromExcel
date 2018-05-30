#! /usr/bin/python3.5
#coding=utf-8
import webbrowser
import re
from pyh_custom import *
from config import *

# 代表一个去重后的versionName所对应的所有crashDiv的总数量和id
class CrashDivStatsOfCertainVersionName:

    def __init__(self, strCrashDivId):
        self.strListCrashDivIds = [strCrashDivId];
    pass;

    def addCrashDivId(self, strCrashDivId):
        self.strListCrashDivIds.append(strCrashDivId);
    pass;

    def getCrashDivCount(self):
        return len(self.strListCrashDivIds);
    pass;

    def getCrashDivIds(self):
        return self.strListCrashDivIds;
    pass;

pass;


# 代表一个html网页，用来在浏览器中显示错误统计结果
class WebOutput:

    def __init__(self, strXlsFilePath):
        self.strXlsFileName = strXlsFilePath;
        self.html = PyH(os.path.basename(self.strXlsFileName) + " crash report");

        self.navDivLeft = self.generateNavDivLeft();
        self.html << self.navDivLeft;
        self.navDivRight = self.generateNavDivRight();
        self.html << self.navDivRight;
        self.statsDiv = self.generateStatsDiv();
        self.html << self.statsDiv;
        self.contentDiv = div(id="idContentDiv");
        self.html << self.contentDiv;
        self.curCrashDiv = div();
        # versionName - CrashDivStats的map
        self.dictUniqueVersionNameToCrashDivStats = {};
        # strCrashOrder - versionNames组成的list的map
        self.dictUniqueCrashOrderToVersionNameLists = {};
        # versionName - crashCount的map
        self.dictUniqueVersionNameToCrashCount = {};
    pass

    # 生成左半边导航栏
    def generateNavDivLeft(self):
        rslt = div(id="idNavDivLeft");
        rslt << h2(os.path.basename(self.strXlsFileName) + " crash report");
        rslt << button("show env stats", id="idBtnEnvStats", visibility="invisible", visibleInnerHTML ="hide env stats", invisibleInnerHTML ="show env stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classEnvStats')");
        rslt << button("show version stats", visibility="invisible", visibleInnerHTML ="hide version stats", invisibleInnerHTML ="show version stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classVersionStats')");
        rslt << button("show crashDate stats", visibility="invisible", visibleInnerHTML ="hide crashDate stats", invisibleInnerHTML ="show crashDate stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classCrashDateStats')");
        rslt << br();
        rslt << button("show user stats", visibility="invisible", visibleInnerHTML ="hide user stats", invisibleInnerHTML ="show user stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classUserStats')", style="margin-top:10px");
        rslt << button("show crashDateHour stats", visibility="invisible", visibleInnerHTML ="hide crashDateHour stats", invisibleInnerHTML ="show crashDateHour stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classCrashDateHourStats')", style="margin-top:10px");
        rslt << br();
        return rslt;
    pass

    # 生成右半边导航栏
    def generateNavDivRight(self):
        rslt = div(id="idNavDivRight");
        self.navDivRightTable = table();
        self.navDivRightTableCurRow = None;
        rslt << self.navDivRightTable;
        return rslt;
    pass

    # 生成统计栏
    def generateStatsDiv(self):
        rslt = div(id="idStatsDiv");
        return rslt;
    pass

    def beginCurCrash(self, strCrashOrder, strRatioPercentage):

        # navDiv2中的链接表的打印
        if(int(strCrashOrder) % OUTPUT_HTML_LINK_TABLE_COL_NUMBER == 1):
            self.navDivRightTableCurRow = tr();
            self.navDivRightTable << self.navDivRightTableCurRow;
        anchorLink = a("crash_" + strCrashOrder + " (" + strRatioPercentage + ")", href="#anchor_" + strCrashOrder, id="anchorLink_" + strCrashOrder);
        tableDataAnchorLink = td();
        tableDataAnchorLink << anchorLink;
        self.navDivRightTableCurRow << tableDataAnchorLink;

        anchor = a(name="anchor_" + strCrashOrder, cl="classAnchor");
        anchor << button("hide crash " + strCrashOrder, id = "button_visibility_" + strCrashOrder, visibility ="visible", visibleInnerHTML ="hide crash " + strCrashOrder, invisibleInnerHTML ="show crash " + strCrashOrder, onclick ="onClickToToggleCrashDivVisibilityById(this, '" + strCrashOrder + "', 'button_highlight_" + strCrashOrder + "', 'anchorLink_" + strCrashOrder + "')");
        anchor << HTML_TAG_SPACE * 4;
        anchor << button("highlight crash " + strCrashOrder, id = "button_highlight_" + strCrashOrder, highlightStatus="off", highlightOnInnerHTML = "unhighlight crash " + strCrashOrder, highlightOffInnerHTML = "highlight crash " + strCrashOrder, onclick="onClickToToggleCrashDivHightlightById(this, '" + strCrashOrder + "', 'button_visibility_" + strCrashOrder + "', 'anchorLink_" + strCrashOrder + "')");
        self.contentDiv << anchor;
        self.curCrashDiv = div(id = strCrashOrder);
        self.contentDiv << self.curCrashDiv;
        self.contentDiv << br();
        self.contentDiv << br();
    pass

    def writeCrashRatioStats(self, strCrashRatioStats, strCrashOrder):
        strCrashRatioStats = re.sub(r"\\n", "<br>", strCrashRatioStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashRatioStats, cl="classCrashRatioStats");
    pass

    def writeEnvStats(self, strEnvStats, strCrashOrder):
        strEnvStats = re.sub(r"\n", "<br/>", strEnvStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strEnvStats, cl="classEnvStats", hidden="hidden");
    pass

    def writeUserStats(self, strUserStats, strCrashOrder):
        strUserStats = re.sub(r"\n", "<br/>", strUserStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strUserStats, cl="classUserStats", hidden="hidden");
    pass

    def writeVersionStats(self, strVersionStats, setVersionNames, strCrashOrder, dictUniqueVersions):

        strVersionStats = re.sub(r"\n", "<br/>", strVersionStats);

        if self.curCrashDiv != None:
            self.curCrashDiv << p(strVersionStats, cl="classVersionStats", hidden="hidden");

            for strVersionName in setVersionNames:
                # 统计整体的去重后的版本名列表
                if strVersionName in self.dictUniqueVersionNameToCrashDivStats:
                    objCrashDivStatsOfCertainVersionName = self.dictUniqueVersionNameToCrashDivStats[strVersionName];
                    objCrashDivStatsOfCertainVersionName.addCrashDivId(strCrashOrder);
                else:
                    self.dictUniqueVersionNameToCrashDivStats[strVersionName] = CrashDivStatsOfCertainVersionName(strCrashOrder);
                # 统计每个crash所对应的versionName
                if strCrashOrder in self.dictUniqueCrashOrderToVersionNameLists:
                    listVersionNames = self.dictUniqueCrashOrderToVersionNameLists[strCrashOrder];
                    if strVersionName not in listVersionNames:
                        listVersionNames.append(strVersionName);
                else:
                    self.dictUniqueCrashOrderToVersionNameLists[strCrashOrder] = [strVersionName];

        for versionName in dictUniqueVersions:
            if versionName in self.dictUniqueVersionNameToCrashCount:
                count = self.dictUniqueVersionNameToCrashCount[versionName];
                count = count + dictUniqueVersions[versionName].count;
                self.dictUniqueVersionNameToCrashCount[versionName] = count;
            else:
                self.dictUniqueVersionNameToCrashCount[versionName] = dictUniqueVersions[versionName].count;

    pass

    def writeCrashDateStats(self, strCrashDateStats, strCrashOrder):
        strCrashDateStats = re.sub(r"\n", "<br/>", strCrashDateStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashDateStats, cl="classCrashDateStats", hidden="hidden");
    pass

    def writeCrashDateHourStats(self, strCrashDateHourStats, strCrashOrder):
        strCrashDateHourStats = re.sub(r"\n", "<br/>", strCrashDateHourStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashDateHourStats, cl="classCrashDateHourStats", hidden="hidden");
    pass

    def writeCrashDateHourSvgHistogram(self, kvListCrashDateHourStatsForHistogram, strCrashOrder):
        svgWidth = (len(kvListCrashDateHourStatsForHistogram) + 1) * CRASH_DATE_HOUR_SVG_IMAGE_PER_HOUR_WIDTH;
        svgHistogram = svg(style="width:{0};height:{1};background:rgb(240,240,240);".format(svgWidth, CRASH_DATE_HOUR_SVG_HEIGHT));
        xPos = CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_LEFT;
        sortedListByCount = sorted(kvListCrashDateHourStatsForHistogram, key=lambda kv:kv[1].count, reverse=True);
        maxCrashCountPerHour = sortedListByCount[0][1].count;

        for strCrashDateHour, objCrashDateHour in kvListCrashDateHourStatsForHistogram:
            timeTextLeftPos = xPos;
            timeTextTopPos = CRASH_DATE_HOUR_SVG_IMAGE_PART_HEIGHT + CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_TOP + CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_BOTTOM;
            lineLeftPos = xPos + 5;
            countTextLeftPos = xPos - 5;

            # 绘制时间文字
            svgHistogram << text(strCrashDateHour, x="{0}".format(timeTextLeftPos), y="{0}".format(timeTextTopPos), fill="black", transform="rotate(90 {0} {1})".format(timeTextLeftPos, timeTextTopPos));

            # 绘制柱子
            lineHeight = round(objCrashDateHour.count * 1.0 / maxCrashCountPerHour * CRASH_DATE_HOUR_SVG_IMAGE_PART_HEIGHT);
            lineTopPos = CRASH_DATE_HOUR_SVG_IMAGE_PART_HEIGHT - lineHeight + CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_TOP;
            svgHistogram << line(x1="{0}".format(lineLeftPos), y1="{0}".format(CRASH_DATE_HOUR_SVG_IMAGE_PART_HEIGHT + CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_TOP), x2="{0}".format(lineLeftPos), y2="{0}".format(lineTopPos), style="stroke:rgb(200, 200, 200);stroke-width:20")

            # 绘制柱子上的次数文字
            svgHistogram << text(str(objCrashDateHour.count), x=str(countTextLeftPos), y="{0}".format(lineTopPos - 5));
            xPos = xPos + CRASH_DATE_HOUR_SVG_IMAGE_PER_HOUR_WIDTH;

        svgDiv = div(cl="classCrashDateHourStats", hidden="hidden", style="overflow:auto");
        svgDiv << svgHistogram;

        self.curCrashDiv << svgDiv;
    pass

    def writeCrashMessage(self, strCrashMessage, strCrashOrder):
        strCrashMessage = re.sub(r"\n", "<br/>", strCrashMessage);
        strCrashMessage = re.sub(r"\t", HTML_TAG_SPACE * 4, strCrashMessage);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashMessage);
    pass

    def printToBrowser(self, strOutputHtmlAbsPath, numTotalCrashes, sameCauseList, otherCause):
        if self.html != None:
            # 写整体versionName复选框
            listUniqueVersionNamesToCrashDivStats = sorted(self.dictUniqueVersionNameToCrashDivStats.items(),
                                                           key=lambda kv: kv[1].getCrashDivCount(), reverse=True)
            checkBoxesDiv = div(cl="classCheckBoxDiv", style="margin-top:10px");
            for (strVersionName, objCrashDivStats) in listUniqueVersionNamesToCrashDivStats:
                # 提取objCrashDivStats中divId列表中的各个divId并拼接成字符串
                strListCrashDivIds = objCrashDivStats.getCrashDivIds();
                strConcatenatedCrashDivIds = "";
                for strCrashDivId in strListCrashDivIds:
                    # 确保这个crashDivId所包含的versionName只有一个，这样才可以加入到versionName筛选中
                    if strCrashDivId in self.dictUniqueCrashOrderToVersionNameLists:
                        if len(self.dictUniqueCrashOrderToVersionNameLists[strCrashDivId]) == 1:
                            strConcatenatedCrashDivIds = strConcatenatedCrashDivIds + "'" + strCrashDivId + "',";
                strDisplayVersionName = strVersionName;
                if strVersionName.replace("," , "").strip() == "":
                    strDisplayVersionName = "unknown version";
                checkBoxesDiv << input(type="checkbox", name="checkBox_" + strVersionName, checked="true", onclick="onVersionNameCheckBoxClicked(this, " + strConcatenatedCrashDivIds + ")");
                checkBoxesDiv << 0 * HTML_TAG_SPACE + strDisplayVersionName + 4 * HTML_TAG_SPACE;

            self.navDivLeft << checkBoxesDiv;

            # 统计选中的versionName的crash总数
            crashCountsStatByVersionName = "";
            for strVersionName in self.dictUniqueVersionNameToCrashCount:
                strDisplayVersionName = strVersionName;
                if strVersionName.replace("," , "").strip() == "":
                    strDisplayVersionName = "unknown version";
                crashCountsStatByVersionName = crashCountsStatByVersionName + strDisplayVersionName + " : " + str(self.dictUniqueVersionNameToCrashCount[strVersionName]) + 30 * HTML_TAG_SPACE;

            self.statsDiv << h3("totalCrashes : " + str(numTotalCrashes) + 20 * HTML_TAG_SPACE + crashCountsStatByVersionName);
            self.statsDiv << h3("specific crash type stats :")

            for sameCause in sameCauseList:
                self.statsDiv << h3(sameCause.toString(numTotalCrashes));
            self.statsDiv << h3(otherCause.toString(numTotalCrashes));

            self.html.addCSS(INPUT_CSS_FILE_PATH);
            self.html.addJS(INPUT_JS_FILE_PATH);
            self.html.printOut(strOutputHtmlAbsPath);
            webbrowser.open(strOutputHtmlAbsPath);
    pass

