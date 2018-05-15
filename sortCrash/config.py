#! /usr/bin/python3.5
#coding=utf-8
import os
import sys

# 确定的各种所需文件路径：
# 输入的文件：test.xls的路径
INPUT_TEST_XLS_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "test.xls");

# 输入的文件：输出的网页所用的js脚本的路径
INPUT_JS_FILE_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "web.js");

# 输入的文件：输出的网页所用的css样式表路径
INPUT_CSS_FILE_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "web.css");

# 网页上crash链接的表格的列数
OUTPUT_HTML_LINK_TABLE_COL_NUMBER = 10;

# 输出的文件：去重后的crash信息暂时存储的目录，为了在命令行中使用，这里用绝对路径
OUTPUT_TMP_DIR_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "tmpDir");

# 输出的文件：html输出的文件名，为了在命令行中使用，这里用绝对路径
# OUTPUT_HTML_FILE_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "tmp.html");

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