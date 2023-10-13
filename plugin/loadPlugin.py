import json
import logging
import os
import re
import time
from importlib import import_module
from Colya.utils.utils import async_call

class Member:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.msg = []

class Group:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.members = {}

class Context:
    def __init__(self) -> None:
        self.groups = {}
        self.members = {}
        self.session = None
    
    def getGroup(self,groupId):
        return self.groups.get(groupId)
    
    def getMember(self,memberId):
        return self.members.get(memberId)
    
    def getGroupMember(self,groupId,memberId):
        return self.groups.get(groupId).members.get(memberId)

class Plugin:
    def __init__(self) -> None:
        # 插件名
        self.name = ""
        # 插件版本
        self.version = ""
        # 插件类型msg|event|setup|task
        self.type = ""
        # 插件触发词（正则）
        self.msg_str=".*"
        # 触发事件
        self.event_type=""
        # 任务循环时间（秒）
        self.task_time=0
        # 启动函数
        self.start_fun = ""

        self.main = None
class Loader:
    def __init__(self) -> None:
        self.path = './plugin'
        self.msgPlugins = []
        self.eventPlugins = []

        self.context = Context()
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
                    self.msgPlugins.append(plugin)
                elif plugin.type == 'event':
                    self.eventPlugins.append(plugin)
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
        plugin.event_type = config.get("event_type","")
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
    def msg(self,fun,context):
        fun(context)

    @async_call
    def event(self,fun,context):
        fun(context)

    def getContext(self,session):
        msg = session.message.content
        if(msg):
            if(session.isGroupMsg):
                group = self.context.groups.get(session.guild.id)
                if not group :
                    group = Group()
                    group.id = session.guild.id
                    group.name = session.guild.name
                    self.context.groups[session.guild.id] = group
                member = self.context.groups.get(session.guild.id).members.get(session.user.id)
                if not member :
                    member = Member()
                    member.id = session.user.id
                    member.name = session.user.name
                    self.context.groups[session.guild.id].members[session.user.id] = member
                self.context.groups[session.guild.id].members[session.user.id].msg.append(msg)
            else:
                member = self.context.members.get(session.user.id)
                if not member :
                    member = Member()
                    member.id = session.user.id
                    member.name = session.user.name
                    self.context.members[session.user.id] = member
                self.context.members[session.user.id].msg.append(msg)
        
        
        context = Context()
        for groupid in self.context.groups:
            group = self.context.groups[groupid]
            for memberid in group.members:
                if memberid == session.user.id:
                    context.groups[groupid] = group
        context.members[session.user.id] = self.context.members.get(session.user.id,{})
        context.session = session
        return context
    
    def matchMsgPlugin(self,session):
        context = self.getContext(session)
        for plugin in self.msgPlugins:
            cp = re.compile(plugin.msg_str)
            match = re.findall(cp,str(session.message.content))
            if match:
                self.msg(plugin.main,context)

    def matchEventPlugin(self,session):
        context = self.getContext(session)
        for plugin in self.eventPlugins:
            if session.type==plugin.event_type:
                self.event(plugin.main,context)
        