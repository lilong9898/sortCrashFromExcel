#! /usr/bin/python3.5
#coding=utf-8
import os
import sys

# 确定的各种所需文件路径：
# 输入的文件：test.xls的路径
INPUT_TEST_XLS_PATH = os.path.realpath(os.path.abspath(os.path.dirname(sys.argv[0])) + os.path.sep + "test.xls");

# 输入的文件：输出的网页所用的js脚本的路径
INPUT_JS_FILE_PATH = os.path.realpath(os.path.abspath(os.path.dirname(sys.argv[0])) + os.path.sep + "web.js");

# 输入的文件：输出的网页所用的css样式表路径
INPUT_CSS_FILE_PATH = os.path.realpath(os.path.abspath(os.path.dirname(sys.argv[0])) + os.path.sep + "web.css");

# 网页上crash链接的表格的列数
OUTPUT_HTML_LINK_TABLE_COL_NUMBER = 10;

# 输出的文件：去重后的crash信息暂时存储的目录，为了在命令行中使用，这里用绝对路径
OUTPUT_TMP_DIR_PATH = os.path.realpath(os.path.abspath(os.path.dirname(sys.argv[0])) + os.path.sep + "tmpDir");

# 输出的文件：html输出的文件名，为了在命令行中使用，这里用绝对路径
# OUTPUT_HTML_FILE_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "tmp.html");

# 小时统计信息的svg画布高度
CRASH_DATE_HOUR_SVG_HEIGHT = "550px";

# 小时统计信息的svg画布的图像部分的高度
CRASH_DATE_HOUR_SVG_IMAGE_PART_HEIGHT = 350;

# 小时统计信息的svg画布的图像部分的顶部留白
CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_TOP = 30;

# 小时统计信息的svg画布的图像部分的底部留白
CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_BOTTOM = 10;

# 小时统计信息的svg画布的左侧留白
CRASH_DATE_HOUR_SVG_IMAGE_PART_MARGIN_LEFT = 30;

# 小时统计信息的svg画布的每小时图像宽度
CRASH_DATE_HOUR_SVG_IMAGE_PER_HOUR_WIDTH = 50;

# html空格符
HTML_TAG_SPACE = "&nbsp;";

# excel表中android sdk列序号
EXCEL_COL_INDEX_ANDROID_VERSION = 0;

# excel表中packageName列序号
EXCEL_COL_INDEX_PACKAGE_NAME = 1;

# excel表中渠道号的列序号
EXCEL_COL_INDEX_CHANNEL_ID = 2;

# excel表中rom列序号
EXCEL_COL_INDEX_ROM = 3;

# excel表中versionCode列序号
EXCEL_COL_INDEX_VERSION_CODE = 4;

# excel表中屏幕大小列序号
EXCEL_COL_INDEX_LCDTYPE = 5;

# excel表中客户端source列序号
EXCEL_COL_INDEX_CLIENT_SOURCE = 6;

# excel表中崩溃信息列序号
EXCEL_COL_INDEX_CRASH = 7;

# excel表中versionName列序号
EXCEL_COL_INDEX_VERSION_NAME = 8;

# excel表中手机类型列序号
EXCEL_COL_INDEX_PHONE_MODEL = 9;

# excel表中id所在列序号
EXCEL_COL_INDEX_ID = 10;

# excel表中崩溃时间列序号
EXCEL_COL_INDEX_CRASH_DATETIME = 11;

# excel表中i号所在的列序号
EXCEL_COL_INDEX_I_ACCOUNT = 12;

# excel表中screenish所在的列序号
EXCEL_COL_INDEX_SCREENISH = 13;

# excel表中othermsg所在的列序号
EXCEL_COL_INDEX_OTHER_MSG = 14

# excel表中的内部版本号所在列序号
EXCEL_COL_INDEX_INTERNAL_APP_VERSION = 15;

# excel表中上传时间所在列序号
EXCEL_COL_INDEX_UPLOAD_TIME = 16;

# 识别崩溃信息的来源，是否为插件的，是哪个插件的，是通过对照崩溃信息和下面表中的关键词来确定的
CRASH_SOURCE_PLUGINS = {
    "插件search":
        ("pluginweb_search", "com.zhangyue.iReader.search", "com.zhangyue.iReader.common.webservice"),
    "插件bookdetail":
        ("pluginwebdiff_bookdetail", "com.zhangyue.iReader.bookDetail", "com.zhangyue.fastjson"),
    "插件bookshelfcard":
        ("pluginwebdiff_bookshelfcard", "com.zhangyue.digest", "com.zhangyue.subscribe"),
    "插件bookstore":
        ("pluginwebdiff_bookstore", "com.zhangyue.bookstore", "com.zhangyue.itemview", "com.zhangyue.scrollheader", "com.zhangyue.timer"),
    "插件bookstore2":
        ("pluginwebdiff_bookstore2", "com.zhangyue.bookstore2"),
    "插件bookstore3":
        ("pluginwebdiff_bookstore3", "com.zhangyue.iReader.common"),
    "插件common":
        ("pluginwebdiff_common", "com.zhangyue.aac", "com.zhangyue.common"),
    "插件config":
        ("pluginwebdiff_configOppo", "com.zhangyue.iReader.plugin.config"),
    "插件mine":
        ("pluginwebdiff_mineOppo", "com.zhangyue.iReader.mine"),
    "插件pdf":
        ("pluginwebdiff_pdf", "com.zhangyue.iReader.PDF", "com.zhangyue.iReader.PDF2"),
}
