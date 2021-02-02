# GetData(CLI)

Python版本 3.8

![](https://img.shields.io/badge/Python-3.8-yellow.svg?style=flat&logo=python)

## 功能

基于AV Data Capture 项目,在其基础之上修改，根据刮削器取得的影片数据修改文件名称为：番号-演员-标题，直接将配置文件设定的movie_folder路径中的影片重新命名。建议使用者测试后使用，以防不测

## 开发环境构建方法

1.下载[AV Data Capture 4.3.2](https://github.com/yoshiko2/AV_Data_Capture/tree/4.3.2)

2.解压AV Data Capture

3.将专属文件清单[^1]中的文件放入AV_Data_Capture.py同级路径下

4.修改config.ini文件，在[common]节中增加movie_folder=XX路径，在[priority]节中website属性中增加javdb7,例如：website = javdb7,javbus,jav321,airav,javdb,fanza,xcity,mgstage,fc2,avsox,javlib,dlsite

5.执行GetData.py即可

## 构建CLI
执行GetData.ps1后，从dist目录中获得GetData.exe，与config.ini文件放到相同路径下执行即可


## 专属文件清单

[^1]:专属文件清单

以GetData开头的所有文件，清单如下：

GetData.ps1 

GetData.py 

GetData_Config.py

GetData_core.py

WebCrawler\javdb7.py

## 原始文件

config.ini(修改) 增加了movie_folder属性

##  申明
当你查阅、下载了本项目源代码或二进制程序，即代表你接受了以下条款

* 本软件仅供技术交流，学术交流使用
* **请勿在热门的社交平台上宣传此项目**
* 本软件作者编写出该软件旨在学习 Python ，提高编程水平
* 本软件不提供任何影片下载的线索
* 用户在使用本软件前，请用户了解并遵守当地法律法规，如果本软件使用过程中存在违反当地法律法规的行为，请勿使用该软件
* 用户在使用本软件时，若用户在当地产生一切违法行为由用户承担
* 严禁用户将本软件使用于商业和个人其他意图
* 源代码和二进制程序请在下载后24小时内删除
* 本软件作者保留最终决定权和最终解释权
* 若用户不同意上述条款任意一条，请勿使用本软件
---
