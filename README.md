# Neo4jVision
# Neo4jVision
---
highlight: a11y-dark
theme: smartblue
---
# 0 版本
```
python == 3.8.0
Django == 4.1.2
py2neo == 2021.2.3
pyecharts == 1.9.1
```
# 1 目的及功能
**目的：** 由于neo4j自带的可视化界面展示效果有限，重建可视化界面  
**功能：** 实现与neo4j数据库实时连接，可动态更新，动态显示

# 2 Neo4j
## 2.1 Neo4安装
在Neo4j官网[下载](https://neo4j.com/download-center/#community)社区版

```
./neo4j console
```


![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/07001ea8fc954b5693e02f041b7a0cd2~tplv-k3u1fbpfcp-watermark.image?)
包涵136个节点，150组关系。 输入查询语句 `MATCH(n) RETURN n` 输出所有节点和关系
# 3 前后端控制
使用Django进行后端控制，Echarts进行前端显示。参考`[3]`项目结构

## 3.1 Django后端
后端使用Django控制，对view进行改写，增加分类 `view.py`文件内容

## 3.2 Echarts前端
`index.html`

# 4 项目启动
进入到主目录文件夹下，运行`manage.py`启动项目，输入命令行:
```
python manage.py runserver
```
`manage.py`中的内容
```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neo4jconnect_test.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```
默认启动地址和端口为：`http://127.0.0.1:8000/` 若希望指定ip地址和端口，可按格式：
```
python manage.py runserver --host 0.0.0.0 --port 9008
```
`--host`参数是ip地址，`--port`参数是端口号

# 遇到问题
## echarts问题
1.加载`echarts.min.js`需要确定好路径  
2.初始化要定义好dom，即，`div中的id`定义要和`getElementById`方法中初始化名称一致。否则会报错误 `t is null`  
```
<div id="chart-panel" style="height: 100%;width: 100%;overflow: hidden;"></div>

...

var dom = document.getElementById("chart-panel");
var myChart1 = echarts.init(dom);
```
3.导入data和link时，要确保数据中**没有重复字段**，否则会造成节点和连线都不显示  
4.保证link中的target和source都是**字符串**类型

## 数据问题
1.导入neo4j中的数据，要避免重复字段。错误示例：实体名称和类名称一致

# 参考
[1] https://github.com/liuhuanyong/QASystemOnMedicalKG  
[2] https://github.com/wangle1218/KBQA-for-Diagnosis  
[3] https://github.com/Sjyzheishuai/Neo4j-visualization  
[4] https://blog.csdn.net/Fimooo/article/details/103069928  
[5] https://blog.csdn.net/weixin_44747173/article/details/124835406  
[6] https://blog.csdn.net/zjw120/article/details/124194577  
[7] https://github.com/zhangxiang0316/echartsDemo  
[8] https://github.com/pyecharts/pyecharts-gallery  
[9] https://github.com/ecomfe/awesome-echarts  
