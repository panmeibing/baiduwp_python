# baiduwp_python


#### 1.说明

baiduwp_python是一个解析百度网盘下载链接的项目，设计思路来自Pandownload，功能是解析已分享的百度网盘链接，得到真实下载链接并可以在下载器进行下载，从而绕过百度网盘客户端。



#### 2.实现思路
本项目思路来自Pandownload，由于百度网盘限速，所以要使用自己的会员账号获取真实下载链接，不存在任何破解行为，请勿用于任何商业行为。本项目使用的接口来自[百度网盘开放平台](https://pan.baidu.com/union)以及[百度网盘网页端](https://pan.baidu.com/)，另外也参考了GitHub项目[百度网盘API](https://github.com/ly0/baidupcsapi)、[baiduwp-php](https://github.com/yuantuo666/baiduwp-php)、[网盘直链下载助手](https://github.com/syhyz1990/baiduyun)等开源项目，感谢各位大佬的贡献。

##### 2.1 项目框架
django + mysql + redis

##### 2.2 基础功能
- 解析下载链接
- 管理网盘账号（cookie）
- 定时查询账号是否可用
- 设置邀请码限流
- 记录访问流量



#### 3.运行项目

这是在本地运行此项目，并非生产环境，如需要部署到生产环境，请用uwsgi、gunicorn等方式进行部署，因步骤过多，此处不进行介绍

##### 3.1 运行环境
Python3.9、Django4.x、Django-redis5.x

```
pip install django==4.1.7
pip install django-redis==5.2.0
pip install redis==4.5.1
pip install apscheduler
pip install selenium
pip install requests
pip install mysqlclient
```

##### 3.2 下载项目
```
git clone https://github.com/panmeibing/baiduwp_python.git
```

##### 3.3 数据库设置
打开项目里的settings.py，修改DATABASES和CACHES两个字典，把ip端口、用户密码等信息修改正确
文件位置：./baiduwp_python/baiduwp_python/settings/settings.py

##### 3.4 迁移
迁移就是指创建数据表，在创建数据表之前要先登录mysql创建数据库
```
CREATE DATABASE `baiduwp` DEFAULT CHARACTER SET utf8mb4;
```
通过Django迁移生成数据表
```
cd baiduwp_python
python manage.py makemigrations
python manage.py migrate
```

##### 3.5 创建超级管理员

超级管理员用于管理数据表的数据，比如说添加或修改网盘账号

```
python manage.py createsuperuser
```

##### 3.6 运行项目

```
python manage.py runserver 
```
在浏览器访问 
主页： http://127.0.0.1:8000/
管理：http://127.0.0.1:8000/admin/
