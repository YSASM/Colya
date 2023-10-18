<h1 align="center"> Colya BOT </h1>
<div align="center">v0.1.0</div>
</div>


***


## 安装：


```
git clone https://gitee.com/YSASM/Colya.git
```


## 配置：

* 创建bot主目录，编写一个启动文件

* 直接把Colya放进bot的主目录



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
    |-console.bat
    |-console.sh
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
    "session_exp_ts":3600，
    "console_service":True//是否开启console服务端
}
```
* 执行console.bat或console.sh需要先设置http_service为True并且确认已经安装了nodejs环境,服务器端请开启7796端口和8080端口
* 由于技术原因未实现config配置console端口,如需变更端口，自行修改代码或者使用nginx等工具

## 编写插件
* 在plugin文件夹中创建你的插件目录，在插件目录下创建config.json和main.py，放在目录里就能加载出来，不用声明其他东西
plugin下每个文件夹为一个插件
```
bot-
    |-main.py
    |-Colya
    |-log--bot.log
    |-plugin-|-newPlugin-|-main.py
             |           |-config.json
             |
             |-newPlugin2-|-main.py
                          |-config.json
```

* 编写config.json(没有config.json时所有参数均为默认值)
```
示例
{
    "name":"newPlugin",//插件名称（目前没用）
    "version":"0.1",//插件版本（目前没用）
    "type":"event",//插件类型（event,setup,task）msg表示收到消息会运行的，setup是开始就运行的，task是定时任务不填默认event
    "match_content":".*"//插件类型为event时生效，填入正则表达式，收到消息匹配成功时运行插件,不填不过滤
    "task_time":1000//插件类型为task时生效，为定时任务间隔时间（秒）,默认10
    "event_type":["message-created"]//插件类型为event时生效，触发事件不填不过滤
    "start_fun":"main",//启动函数（在main.py中的启动函数的函数名）不填默认main
    "cmd_fun":"cmd",//启动函数（在main.py中的命令函数的函数名）不填默认cmd
    "file_name":"main",//启动函数所在的文件名，不填默认main
    "pass_group":["123","123123"]//生效群号，不填对所有群生效
    "pass_friend":["123123","123"]//生效id，不填对所有人生效
    "cmd_help":["/newPlugin [xxx参数] [xxx参数]"],//命令提示
    "off":"False"//是否关闭插件
}
```
* 编写main.py(file_name.py)
```
//SendMessage为发送消息的类
from  Colya.service.MessageService import SendMessage,setMsgSession
//此处main为config.json中配置的start_fun
from Colya.plugin.base import PluginBase
//type为event时主函数要接收一个context，setup和task没有参数
def main(context):
    //先调用一下base格式化context信息
    //context中包含session(触发事件的所有参数信息)和历史session信息
    base = PluginBase(context)
    //dictionary中有所有功能的实现方式
    base.dictionary.MessageCreate(base.session_guild_id,"测试回复").do()

--------------------------------------------------------------------------
可以单独调用Dictionary
from Colya.dictionary import Dictionary
def main():
    dict = Dictionary()
    dict.MessageCreate('群号','内容').do()

------------------------------------------------------------------------------
//示例
from Colya.plugin.base import PluginBase
from Colya import logging
def main(context):
    base = PluginBase(context)
    logging.info(base.session_content)
def cmd(cmd,*args):
    logging.info(cmd)

```

## 日志
```
from Colya import logging
logging.info("xxx")
logging.warn("xxx")
logging.error("xxx")
//logging.text只有在console_service开启时可用
logging.text("xxx")
```

## 以实现功能

- [x] 接收发送消息
- [x] 动态加载插件
- [x] 插件config
- [x] console控制台





## 感谢
 
* 框架由https://github.com/kumoSleeping/TomorinBot提供技术参考

