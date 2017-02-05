# stttt2003pk_f5_config_read

## Introduction

* stttt2003pk_f5_config_read是我在做运维工具开发和实施运维变更过程中对F5的配置做的一个底层库
* 该库的主要作用是提取配置至内存，形成字典的数据结构，方便导入CMDB和进行更多的配置分析，比如配置合规性检查，配置数目的统计等。
* 这么做的主要原因是我们新的任务工作平台都是通过现在[比较流行的devops的形式去进行部署实施的](https://github.com/stttt2003pk/stttt2003pk_lvs_manager)，但是难免会遇到一些老的项目，老的配置文件需要重新去进行迁移和整理，在我的工作当中这些就包括了lvs/nginx/haproxy/f5/cisco/apache等服务器相关应用的相关配置，在原来规划比较混乱配置比较难以处理的情况下，通过这种底层库的编写能够准确的通过文件读取配置文件的具体内容，形成kv或者json的形式供我们插入到CMDB当中，实现新老业务的过度。
* 通过正则表达式分析文件内容，并且经过内存处理后，我们能充分利用这些资源进行更多的动作，在我的工作当中如进行配置分析、配置整改、生成相关的命令行等，在这个仓库当中都能够体现
* 通过这种形式分析的lvs/nginx/apache/haproxy配置文件都非常容易编写，需要的可以联系 414150392@qq.com

## Core Code Share

### Build the structure

* 让熟悉业务的运维人员创造相关的数据结构

[像文件里面这样，可以通过更简单的数据结构，这个脚本在一开始没有规划的很好，所以都是以类的形式创建](https://github.com/stttt2003pk/stttt2003pk_f5_config_read/blob/master/F5ToolPackage/F5_Parameter.py)

### Using Regular Expression

* 注意区分版本，比如F5有10 11等几个大版本，不同模块的配置文件形式也不同；cisco有ios、iox、nxos也会有很多不同，但是通过正则都能很好封装

[像这样](https://github.com/stttt2003pk/stttt2003pk_f5_config_read/blob/master/F5ToolPackage/ReadLtmConfigInToRamV11.py)

### Using The Gathered Data

* [接下啦可以更好的去规划需要的配置](https://github.com/stttt2003pk/stttt2003pk_f5_config_read/blob/master/F5SearchToolFunction/ConfigSearchFunctions.py)
* 封装我们需要的需求比如查找，生成命令行等。
* 其实每个厂家都会有比较好的操作库，比如F5的icontrol的接口，比如saltstack现在也对各个module进行了很好的封装，**自己造轮子主要为了更个性化的需求**比如我们去年做的一个项目将所有nginx/IIS/tomcat上面的ssl配置移动到F5上面去做，这个预先的工作就帮了很大的忙

### Test

* 杂乱无章的配置都整理成为json了

![](https://raw.github.com/stttt2003pk/stttt2003pk_f5_config_read/master/screenshot/json.png)