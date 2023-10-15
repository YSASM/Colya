


<h1 align="center"> Colya BOT </h1>
<!-- <div align="center"> <img src="./logo.jpg" width="120"/> </div> -->
<div align="center">v0.1.0</div>
<!-- <div align="center">  人間になりたいうた... -->
</div>


***


## 安装：


```
git clone https://gitee.com/YSASM/Colya.git
```


## 配置：

* 运行setup.py或者直接把Colya放进bot的主目录

* 创建波特主目录，编写一个启动文件

```
bot-
    |-main.py
    |-Colya
```

```
main.py

from Colya.bot import Bot
bot = Bot()
bot.run()
```

* 然后运行main.py，就会将整个文件目录创建好
```
bot-
    |-main.py
    |-Colya
    |-log--bot.log
    |-plugin
```

* 然后填写config.json文件,填写token即可
```
{
    "host": "127.0.0.1", 
    "port": "5500", 
    "token": "", 
    //心跳间隔
    "heart_beat_cd": 60,
    //历史session过期事件(秒)
    "session_exp_ts":3600
}
```

## 编写插件
* 在plugin文件夹中创建你的插件目录，在插件目录下创建config.json和main.py
plugin下每个文件夹为一个插件
```
bot-
    |-main.py
    |-Colya
    |-log--bot.log
    |-plugin-|-newPlugin-|-main.py
             |           |-config.json
             |
```          |-newPlugin2-|-main.py
                          |-config.json

* 编写config.json(没有config.json时所有参数均为默认值)
```
示例
{
    "name":"newPlugin",//插件名称（目前没用）
    "version":"0.1",//插件版本（目前没用）
    "start_fun":"main",//启动函数（在main.py中的启动函数的函数名）不填默认main
    "file_name":"main",//启动函数所在的文件名，不填默认main
    "type":"event",//插件类型（event,setup,task）msg表示收到消息会运行的，setup是开始就运行的，task是定时任务不填默认event
    "event_type":["message-created"]//插件类型为event时生效，触发事件不填不过滤
    "match_content":".*"//插件类型为event时生效，填入正则表达式，收到消息匹配成功时运行插件,不填不过滤
    "task_time":1000//插件类型为task时生效，为定时任务间隔时间（秒）,默认10
    "pass_group":["123","123123"]//生效群号，不填对所有群生效
    "pass_friend":["123123","123"]//生效id，不填对所有人生效
}
```
* 编写main.py(file_name.py)
```
//SendMessage为发送消息的类
from  Colya.service.MessageService import SendMessage,setMsgSession
//此处main为config.json中配置的start_fun
from Colya.plugin.base import PluginBase
//主函数要接收一个context
def main(context):
    //先调用一下base格式化context信息
    //context中包含session(触发事件的所有参数信息)和历史session信息
    base = PluginBase(context)
    //dictionary中有所有功能的实现方式
    base.dictionary.MessageCreate(base.session_guild_id,"测试回复").do()

```

## 以实现功能

* 发送消息

## 感谢
 
* 框架由https://github.com/kumoSleeping/TomorinBot提供技术参考

