# GZCTF_BOT

一款适用于GZ::CTF平台可控制的QQ播报BOT，由于平台的API调用十分方便，使用BOT的可优化的功能点有很多。GZtime nb.jpg！！！

### 功能🧀

- Blood播报（First Blood、Second Blood、Third Blood）
- 题目上新播报
- 题目提示更新播报
- 赛事公告播报
- 播报可控开关
- 多比赛同时监控
- 可方便的为用户配置权限
- 可方便的设置消息发送终点
- 定制型消息模板（让你的公告与众不同 qwq）
- 拥有较好的拓展性

### 使用教程 🚗

1. 根据部署过程安装Nonebot2、go-cqhttp 的相关依赖；
2. 使用git指令拉取本仓库的源码放置你所指定的目录；
3. 修改部署过程中的指定参数，比如QQ号，平台地址等需要自定义的参数；
4. 移动到**go-cqhttp**目录使用`nohup go-cqhttp >/dev/null 2>&1 &`放在后台运行，如果实在调试过程中就不需要放置后台运行；
5. 回到**bot.py**所在目录，使用 `nohup python3 bot.py >/dev/null 2>&1 &`后台运行bot.py;
6. 由指定的白名单用户对QQ-bot用户发出`/open`指令开启bot，配置无误将会收到“播报已经开启”的回复；
7. 回到本项目点一个star，后续将陆续开发出新功能，尽情期待！

使用白名单用户向机器人发送 /help 或者 /帮助来查看帮助（功能很少Orz）

### 部署过程 🚀

此服务使用 **Nonebot2 + go-cqhttp** 架构完成搭建，需要一点点python基础。

#### 搭建go-cqhttp 🤖

首先前往 [go-cqhttp 下载页面](https://github.com/Mrs4s/go-cqhttp/releases) 下载并安装 **`go-cqhttp`** 最新版本

使用 **go-cqhttp** 进行初始化，选择如下

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/c4796e35-9592-4481-b1ef-4ad42c59c70e)

初始化后，打开同目录下的 `config.yml` 文件，配置好自己的登录令牌，密码可选择为空，然后使用扫码进行登录

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/375b00a7-78c3-45d3-90a6-d9759793eedc)

同时，在 `config.yml` 文件中找到 `ws-server` 设置项，进行如下设置

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/8a8aa999-845e-4c78-aaf1-dfdd67369ff2)

打开同目录下的 `device.json` 将 **`protocol`** 项更改为2（Android Watch协议）

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ffce8a38-3bef-4efe-9351-9c12182aa8f3)

最后再次使用 `go-cqhttp` 指令，使用二维码即可登录自己的qq，并实现命令行接收qq信息

也可以直接使用 `go-cqhttp` 提供的API实现消息的发送与接收，详细请前往 [go-cqhttp 官方文档](https://docs.go-cqhttp.org/api/#%E5%9F%BA%E7%A1%80%E4%BC%A0%E8%BE%93)

#### 部署Nonebot2 🐱‍🐉

首先安装相关依赖
```
python3 -m venv .venv
source .venv/bin/activate
pip install nb-cli==1.4.1
pip install nonebot2==2.3.2
pip install nonebot-adapter-cqhttp==2.0.0b1
pip install pydantic==1.10.15
nb plugin install nonebot_plugin_apscheduler
nb driver install fastapi
```
然后使用git拉取GZCTF-BOT项目到你指定的文件夹中

![截图](https://github.com/Birkenwald-Sec/GZCTF-BOT/assets/61536775/ba18028c-4ddc-47b6-abf2-c9ff10d3cb60)

设置 **GZCTF-BOT/src/plugin/gzctf-plugin/config.py** 中的必选项，然后使用 python 启动 bot.py 即可

#### config.py 设置 🔧

- "WHITE_LIST": 规定指令监听消息的来源
  - "key": 可触发指令的用户的账号
  - "value"
    - "type": "private", "group", "all"
      - "private": 表示监听单个用户，设置此项则后续 `group` 项无效
      - "group": 该类型表示监听群组消息， 设置此项则必须设置后续的 `group` 项来指明被监听群的群号
      - "all": 该类型表示既监听私人信息又监听群组消息，设置此项则必须设置后续的 `group` 项
      - "注": 所监听的私人用户账号是上面所设置 "key" 字段
    - "group": 列表，其中添加被监听群的群号，需使用字符串格式 
``` python
# WHITE_LIST 标准示例
"WHITE_LIST" : {
            "1234567890": {"type": "all","group":['518041028']},
            "2236548876": {"type": "private"}
        }
```

- "ENDPOINT": 用来指明消息接收方
  - "group_id": 列表，指明接收群群号
  - "user_id": 列表，指明接收用户的账号

``` python
# ENDPOINT 标准示例
"ENDPOINT" : {
            'group_id': [518041028],
            'user_id': [1234567890]
        }
```

- "BC_FRESH_TIME": 播报刷新频率，可空，默认20秒一次

- "GAMEMONITORED": GZCTF比赛标题，可使用列表指定多个

``` python
# GAMEMONITORED 标准示例
"GAMEMONITORED" : ["myCtf1","myCtf2","myCtf3",...]
```

![image](https://github.com/Birkenwald-Sec/GZCTF-QQBOT/assets/61536775/82afe583-1acf-4842-8e5c-4ffd96ce313c)

- "BC_MESSAGE_TEMPLATE": 播报消息模板
  - "{type}": 表示消息种类
  - "{time}": 表示消息发生时间
  - "{content}": 表示消息内容
  - "{year}": 消息时间 - 年
  - "{month}": 消息时间 - 月
  - "{day}": 消息时间 - 日
  - "{hour}": 消息时间 - 时
  - "{minute}": 消息时间 - 分
  - "{second}": 消息时间 - 秒
  - "{game_title}": 比赛标题
  - "{game_id}": 比赛id号
  - "注": 可从 [CQ码](https://docs.go-cqhttp.org/cqcode/#%E8%BD%AC%E4%B9%89) 获取表情字符使用说明

``` python
# BC_MESSAGE_TEMPLATE 标准示例
"类型：{type} 于 {game_title}\n内容： {content}\n时间： {month}-{day} {time}"
```

![image](https://github.com/Birkenwald-Sec/GZCTF-QQBOT/assets/61536775/0ba51842-ef88-4177-bb6b-5bee48e757cd)

![image](https://github.com/Birkenwald-Sec/GZCTF-QQBOT/assets/61536775/d998f09a-d3e3-4528-b23b-ddea0f784050)

- "GZCTF_USER": GZCTF平台管理员账户

- "GZCTF_USER_PASS": GZCTF平台管理员密码

- "BASEURL": gzctf平台地址，例：https://www.gzctf.com/

设置完上述参数后 使用 python运行 bot.py文件即可，如果需要设置为后台运行可以使用 `nohup python3 bot.py >/dev/null 2>&1 &`

**注： GAMEMONITORED 中指定的比赛需要被开启才能够被监听！**

**注： 机器人部署好之后，可根据自己指定的权限用户向机器人发送 '/帮助' 或 '@你的机器人ID /帮助' 来获取指令帮助手册**
