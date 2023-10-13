import json
import logging
import os
import re
import time
from importlib import import_module
from Colya.utils.utils import async_call

class Plugin:
    def __init__(self) -> None:
        # 插件名
        self.name = ""
        # 插件版本
        self.version = ""
        # 插件类型msg|setup|task
        self.type = ""
        # 插件触发词（正则）
        self.msg_str=".*"
        # 任务循环时间（秒）
        self.task_time=0
        # 启动函数
        self.start_fun = ""

        self.main = None
class Loader:
    def __init__(self) -> None:
        self.path = './plugin'
        self.plugins = []
    def load(self):
        logging.info('------加载插件------')
        files = os.listdir(self.path)
        for file in files:
            try:
                config = json.load(open(f'{self.path}/{file}/config.json'))
                plugin = self.getPlugin(config)
                module = import_module(name=f"plugin.{file}.main")
                plugin.main = getattr(module, plugin.start_fun)
                if plugin.type == 'msg':
                    self.plugins.append(plugin)
                elif plugin.type == 'setup':
                    self.setup(plugin.main)
                elif plugin.type == 'task':
                    self.task(plugin.main,plugin.task_time)
            except Exception as e:
                logging.error(f"[加载插件出错]{e}")
        logging.info('------插件加载完毕------')
    
    def getPlugin(self,config) -> Plugin:
        plugin = Plugin()
        plugin.name = config.get("name","")
        plugin.version = config.get("version","")
        plugin.type = config.get("type","")
        plugin.msg_str = config.get("msg_str","")
        plugin.task_time = config.get("task_time",0)
        plugin.start_fun = config.get("start_fun","")
        return plugin
    
    @async_call
    def setup(self,fun):
        fun()

    @async_call
    def task(self,fun,num):
        while True:
            fun()
            time.sleep(num)
    
    @async_call
    def msg(self,fun,session):
        fun(session)
    
    def matchMsgPlugin(self,session):
        msg = session.message.content
        for plugin in self.plugins:
            if re.match(plugin.msg_str,msg):
                self.msg(plugin.main,session)
        