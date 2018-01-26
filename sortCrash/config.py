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
OUTPUT_HTML_FILE_PATH = os.path.realpath(os.path.dirname(sys.argv[0]) + os.path.sep + "tmp.html");

# html空格符
HTML_TAG_SPACE = "&nbsp;";

# excel表中android sdk列序号
EXCEL_COL_INDEX_ANDROID_SDK = 0;

# excel表中packageName列序号
EXCEL_COL_INDEX_PACKAGE_NAME = 1;

# excel表中渠道号的列序号
EXCEL_COL_INDEX_CHANNEL_ID = 2;

# excel表中rom列序号
EXCEL_COL_INDEX_ROM = 3;

# excel表中versionCode列序号
EXCEL_COL_INDEX_VERSION_CODE = 4;

# excel表中崩溃信息列序号
EXCEL_COL_INDEX_CRASH = 7;

# excel表中versionName列序号
EXCEL_COL_INDEX_VERSION_NAME = 8;

# excel表中崩溃时间列序号
EXCEL_COL_INDEX_CRASH_TIME = 11;

# excel表中的用户名(即i号)列序号
EXCEL_COL_INDEX_USER_NAME = 12;

# 过滤掉的关键字
EXCLUDE_KEY_WORDS = ();