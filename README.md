# YouMing BBS

YouMing BBS is an online bulletin board system.

PKU JsWeb &amp; Database course project

<img src="README.assets\BBS.png" alt="BBS" style="zoom:50%;" />

## Install and Run

#### Mysql database

初始化数据库，在 mysql 中，运行

dbinit/big-large-titanic-tremendous-gigantic.sql

修改 config.py，添加用户名，密码等配置

#### Python environment

python = 3.8

install dependency

```shell
pip install flask flask-login pymysql icecream
```

#### Run

```shell
cd bbs-backend
flask run
```
