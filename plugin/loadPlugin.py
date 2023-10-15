import json
import logging
import os
import re
import time
from importlib import import_module
from Colya.utils.utils import async_call
from Colya.Config.config import Config

config = Config()


class Member:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.sessions = []


class Group:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.members = []


class Context:
    def __init__(self) -> None:
        self.groups = []
        self.members = []
        self.session = None
        self.plugin = None

    def getGroup(self, groupId):
        for group in self.groups:
            if group.id == groupId:
                return group
        return None

    def getMember(self, memberId):
        for member in self.members:
            if member.id == memberId:
                return member
        return None

    def getGroupMember(self, groupId, memberId):
        for group in self.groups:
            if group.id == groupId:
                for member in group.members:
                    if member.id == memberId:
                        return member
                break
        return None

    def setMemberSession(self, memberId, session):
        for index, member in enumerate(self.members):
            # 清理过期session
            temp = []
            for si, msession in enumerate(member.sessions):
                ts = int(time.time())-int(int(msession.timestamp)/1000)
                exp_ts = config.getConfig('session_exp_ts', 3600)
                if ts < exp_ts:
                    temp.append(self.members[index].sessions[si])
            member.sessions = temp
            if member.id == memberId:
                self.members[index].sessions.append(session)
        newmember = Member()
        newmember.id = session.user.id
        newmember.name = session.user.name
        newmember.sessions.append(session)
        self.members.append(newmember)

    def setGroupMemberSession(self, groupId, memberId, session):
        for gi, group in enumerate(self.groups):
            if group.id == groupId:
                for mi, member in enumerate(group.members):
                    # 清理过期session
                    temp = []
                    for si, msession in enumerate(member.sessions):
                        ts = int(time.time())-int(int(msession.timestamp)/1000)
                        exp_ts = config.getConfig('session_exp_ts', 3600)
                        if ts < exp_ts:
                            temp.append(self.groups[gi].members[mi].sessions[si])
                    member.sessions = temp
                    if member.id == memberId:
                        self.groups[gi].members[mi].sessions.append(session)
                        return
                newmember = Member()
                newmember.id = session.user.id
                newmember.name = session.user.name
                newmember.sessions.append(session)
                self.groups[gi].members.append(newmember)
                return
        group = Group()
        group.id = session.guild.id
        group.name = session.guild.name
        self.groups.append(group)
        self.setGroupMemberSession(groupId, memberId, session)


class Plugin:
    def __init__(self) -> None:
        # 插件名
        self.name = ""
        # 插件版本
        self.version = ""
        # 插件类型event|setup|task
        self.type = ""
        # 插件触发词（正则）
        self.match_content = ".*"
        # 触发事件
        self.event_type = ""
        # 任务循环时间（秒）
        self.task_time = 0
        # 启动函数
        self.start_fun = ""
        # 主函数文件名
        self.file_name = ""
        # 限制群聊
        self.pass_group = {}
        # 限制私聊
        self.pass_friend = {}
        # 关闭插件
        self.off = False
        self.main = None


class Loader:
    def __init__(self) -> None:
        self.path = './plugin'
        self.plugins = []

        self.context = Context()

    def load(self):
        logging.info('------加载插件------')
        files = os.listdir(self.path)
        for file in files:
            try:
                try:
                    config = json.load(
                        open(f'{self.path}/{file}/config.json', 'r', encoding='utf-8'))
                except Exception as e:
                    config = {}
                plugin = self.getPlugin(config)
                if plugin.off:
                    continue
                module = import_module(
                    name=f"plugin.{file}.{plugin.file_name}")
                plugin.main = getattr(module, plugin.start_fun)
                if plugin.type == 'event':
                    self.plugins.append(plugin)
                elif plugin.type == 'setup':
                    self.setup(plugin.main)
                elif plugin.type == 'task':
                    self.task(plugin.main, plugin.task_time)
                logging.info(f'------插件{plugin.name or file}加载完毕------')
            except Exception as e:
                logging.error(f"[加载插件出错]{e}")
        logging.info('------插件加载完毕------')

    def getPlugin(self, config) -> Plugin:
        plugin = Plugin()
        plugin.name = config.get("name", "")
        plugin.version = config.get("version", "")
        plugin.type = config.get("type", "event")
        plugin.match_content = config.get("match_content", ".*")
        plugin.task_time = config.get("task_time", 10)
        plugin.event_type = config.get("event_type", [])
        plugin.start_fun = config.get("start_fun", "main")
        plugin.file_name = config.get("file_name", "main")
        plugin.pass_group = config.get("pass_group", [])
        plugin.pass_friend = config.get("pass_friend", [])
        plugin.off = config.get("off", False)
        return plugin

    @async_call
    def setup(self, fun):
        fun()

    @async_call
    def task(self, fun, num):
        while True:
            fun()
            time.sleep(num)

    @async_call
    def event(self, fun, context):
        fun(context)

    def getContext(self, session):
        if (session.message.content and session.isGroupMsg):
            self.context.setGroupMemberSession(
                session.guild.id, session.user.id, session)
        else:
            self.context.setMemberSession(session.user.id, session)

    def copyContext(self):
        context = Context()
        context.groups = self.context.groups
        context.members = self.context.members
        return context

    def matchPlugin(self, session):
        self.getContext(session)
        for plugin in self.plugins:
            cp = re.compile(plugin.match_content)
            if session.message and session.message.content:
                match_c = re.findall(cp, str(session.message.content))
            else:
                match_c = ['pass']
            if session.isGroupMsg:
                if plugin.pass_group:
                    if session.guild.id not in plugin.pass_group:
                        return
                if plugin.pass_friend:
                    if session.user.id not in plugin.pass_friend:
                        return
            else:
                if plugin.pass_friend:
                    if session.user.id not in plugin.pass_friend:
                        return
            if (not plugin.event_type or session.type in plugin.event_type) and match_c:
                context = self.copyContext()
                context.session = session
                context.plugin = plugin
                self.event(plugin.main, context)
