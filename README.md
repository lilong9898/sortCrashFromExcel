# sortCrashFromExcel
### 准备环境：
- 安装python3.5（项目按照python3.5规范编码)
- 下载该项目并安装各个依赖库: xlrd xlwt progressbar 
### 准备输入文件：
- 准备好崩溃统计excel表，如果有mapping文件的话也可以准备
### 运行：
#### 过滤：
- 运行filter_crash.py来过滤输入的崩溃统计excel表，假设名字为crash.xls，输出是在其同级目录生成的一个叫crash_filtered.xls的新表　　
<br>```python3 filter_crash.py crash.xls```
#### 统计：
- 运行sort_crash.py来统计输入的崩溃统计excel表，输出是一个网页（存储在输入的excel表的同级目录下，名字是crash_filtered.html），会自动打开
<br>```python3 sort_crash.py crash_filtered.xls```　　

- 如果需要反混淆，则可以
<br>```python3 sort_crash.py crash_filtered.xls mapping1.txt mapping2.txt ...(可以输入多个mapping文件，方便插件崩溃的retrace)```
### 配置运行参数：
- 目前所有过滤和统计功能的参数都不支持从外部输入，请在filter_crash.py和sort_crash.py源码中按照注释修改后再运行
