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
        self.contentDiv = div(id="idContentDiv");
        self.html << self.contentDiv;
        self.curCrashDiv = div();
        # versionName - CrashDivStats的map
        self.dictUniqueVersionNamesToCrashDivStats = {};
        # strCrashOrder - versionNames组成的list的map
        self.dictUniqueCrashOrderToVersionNameLists = {};
    pass

    # 生成左半边导航栏
    def generateNavDivLeft(self):
        rslt = div(id="idNavDivLeft");
        rslt << h2(os.path.basename(self.strXlsFileName) + " crash report");
        rslt << button("hide env stats", id="idBtnEnvStats", visibility="visible", visibleInnerHTML ="hide env stats", invisibleInnerHTML ="show env stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classEnvStats')");
        rslt << button("hide version stats", visibility="visible", visibleInnerHTML ="hide version stats", invisibleInnerHTML ="show version stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classVersionStats')");
        rslt << button("hide crashDate stats", visibility="visible", visibleInnerHTML ="hide crashDate stats", invisibleInnerHTML ="show crashDate stats", onclick="onClickToToggleElementsVisibilityByClassName(this, 'classCrashDateStats')");
        rslt << br();
        rslt << br();
        return rslt;
    pass

    # 生成右半边导航栏
    def generateNavDivRight(self):
        rslt = div(id="idNavDivRight");
        self.navDivRightTable = table();
        self.navDivRightTableCurRow = None;
        rslt << self.navDivRightTable;
        remainingRatioDiv = div(id="idRemainingRatioDiv");
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
        anchor << button("hide crash " + strCrashOrder, id = "button_" + strCrashOrder, visibility ="visible", visibleInnerHTML ="hide crash " + strCrashOrder, invisibleInnerHTML ="show crash " + strCrashOrder, onclick ="onClickToToggleCrashDivVisibilityById(this, '" + strCrashOrder + "', 'anchorLink_" + strCrashOrder + "')");
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
            self.curCrashDiv << p(strEnvStats, cl="classEnvStats");
    pass

    def writeVersionStats(self, strVersionStats, setVersionNames, strCrashOrder):

        strVersionStats = re.sub(r"\n", "<br/>", strVersionStats);

        if self.curCrashDiv != None:
            self.curCrashDiv << p(strVersionStats, cl="classVersionStats");

            for strVersionName in setVersionNames:
                # 统计整体的去重后的版本名列表
                if strVersionName in self.dictUniqueVersionNamesToCrashDivStats:
                    objCrashDivStatsOfCertainVersionName = self.dictUniqueVersionNamesToCrashDivStats[strVersionName];
                    objCrashDivStatsOfCertainVersionName.addCrashDivId(strCrashOrder);
                else:
                    self.dictUniqueVersionNamesToCrashDivStats[strVersionName] = CrashDivStatsOfCertainVersionName(strCrashOrder);
                # 统计每个crash所对应的versionName
                if strCrashOrder in self.dictUniqueCrashOrderToVersionNameLists:
                    listVersionNames = self.dictUniqueCrashOrderToVersionNameLists[strCrashOrder];
                    if strVersionName not in listVersionNames:
                        listVersionNames.append(strVersionName);
                else:
                    self.dictUniqueCrashOrderToVersionNameLists[strCrashOrder] = [strVersionName];
    pass

    def writeCrashDateStats(self, strCrashDateStats, strCrashOrder):
        strCrashDateStats = re.sub(r"\n", "<br/>", strCrashDateStats);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashDateStats, cl="classCrashDateStats");
    pass

    def writeCrashMessage(self, strCrashMessage, strCrashOrder):
        strCrashMessage = re.sub(r"\n", "<br/>", strCrashMessage);
        strCrashMessage = re.sub(r"\t", HTML_TAG_SPACE * 4, strCrashMessage);
        if self.curCrashDiv != None:
            self.curCrashDiv << p(strCrashMessage);
    pass

    def printToBrowser(self):
        if self.html != None:
            # 写整体versionName复选框
            listUniqueVersionNamesToCrashDivStats = sorted(self.dictUniqueVersionNamesToCrashDivStats.items(),
                                            key=lambda kv: kv[1].getCrashDivCount(), reverse=True)
            checkBoxesDiv = div(cl="classCheckBoxDiv");
            for (strVersionName, objCrashDivStats) in listUniqueVersionNamesToCrashDivStats:
                # 提取objCrashDivStats中divId列表中的各个divId并拼接成字符串
                strListCrashDivIds = objCrashDivStats.getCrashDivIds();
                strConcatenatedCrashDivIds = "";
                for strCrashDivId in strListCrashDivIds:
                    # 确保这个crashDivId所包含的versionName只有一个，这样才可以加入到versionName筛选中
                    if strCrashDivId in self.dictUniqueCrashOrderToVersionNameLists:
                        if len(self.dictUniqueCrashOrderToVersionNameLists[strCrashDivId]) == 1:
                            strConcatenatedCrashDivIds = strConcatenatedCrashDivIds + "'" + strCrashDivId + "',";
                checkBoxesDiv << input(type="checkbox", name="checkBox_" + strVersionName, checked="true", onclick="onVersionNameCheckBoxClicked(this, " + strConcatenatedCrashDivIds + ")");
                checkBoxesDiv << 0 * HTML_TAG_SPACE + strVersionName + 4 * HTML_TAG_SPACE;

            self.navDivLeft << checkBoxesDiv;

            self.html.addCSS(INPUT_CSS_FILE_PATH);
            self.html.addJS(INPUT_JS_FILE_PATH);
            self.html.printOut(OUTPUT_HTML_FILE_PATH);
            webbrowser.open(OUTPUT_HTML_FILE_PATH);
    pass

