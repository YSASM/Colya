


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

## 编写插件
* 在plugin文件夹中创建你的插件目录，在插件目录下创建config.json和main.py
```
bot-
    |-main.py
    |-Colya
    |-log--bot.log
    |-plugin--newPlugin-|-main.py
                        |-config.json
```

* 编写config.json
```
示例
{
    "name":"newPlugin",//插件名称（目前没用）
    "version":"0.1",//插件版本（目前没用）
    "start_fun":"main",//启动函数（在main.py中的启动函数的函数名）
    "type":"msg",//插件类型（msg,setup,task）msg表示收到消息会运行的，setup是开始就运行的，task是定时任务
    "msg_str":".*"//插件类型为msg时生效，填入正则表达式，收到消息匹配成功时运行插件
    "task_time":1000//插件类型为task时生效，为定时任务间隔时间（秒）
}
```
* 编写main.py
```
//SendMessage为发送消息的类
from  Colya.service.MessageService import SendMessage,setMsgSession
//此处main为config.json中配置的start_fun
def main(session):
    //初始化SendMessage传入一个session如果是回复消息直接回传main收到的session
    //主动发送需要调用setMsgSession构建一个session即可
    sender = SendMessage(session)
    sender.send_string('收到消息'+session.message.content)
```

## 以实现功能

* 发送消息

## 感谢
 
* 框架由https://github.com/kumoSleeping/TomorinBot提供技术参考

