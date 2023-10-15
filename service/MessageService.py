import json
import logging
import re

import requests
from Colya.Config.config import Config
from Colya.utils.utils import async_call,msgFormat
from Colya.plugin.loadPlugin import Loader
# from Colya import Manager
class MessageService:
    def __init__(self) -> None:
        self.pluginLoader = Loader()
    @async_call
    def receive(self,msg):
        # data = json.loads(message)
        # 这里直接unescape_special_characters可能会导致混淆
        data = json.loads(msgFormat(msg))
        # print("Dev中信息：", data)
        if data['op'] == 4:
            platform = data['body']['logins'][0]['platform']
            bot_name = data['body']['logins'][0]['user']['name']
            self.pluginLoader.load()
            logging.info(f"Satori服务已连接，{bot_name} 已上线 [{platform}] ！")
            # Manager.start()
        elif data['op'] == 0:
            session = Session(data["body"])
            user_id = session.user.id
            try:
                self.pluginLoader.matchPlugin(session)
            except Exception as e:
                logging.error("插件运行出错:",e)
            try:
                member = session.user.name
                if not member:
                    member = f'QQ用户{user_id}'
            except:
                # 为什么是QQ用户，因为就QQ可能拿不到成员name...
                member = f'QQ用户{user_id}'
            content = f"['触发事件:'{str(session.type)}][{str(session.guild.name)+'|'+member if session.isGroupMsg else member}]{str(session.message.content)}"
            # logging.info(( {member} )" + session.message.content)
            logging.info(content)
            
        elif data['op'] == 2:
            # print('[心跳状态：存活]')
            logging.info("心跳存活")



class Session:
    def __init__(self, body):
        self.id = body.get('id')
        self.type = body.get('type')
        self.platform = body.get('platform')
        self.self_id = body.get('self_id')
        self.timestamp = body.get('timestamp')
        self.channel = Channel(body.get('channel', {}))
        self.guild = Guild(body.get('guild', {}))
        self.member = body.get('member', {})
        self.message = Message(body.get('message', {}))

        self.user = User(body.get('user', {}))
        
        
        
        self.isGroupMsg = self.guild.id != None




class setMsgSession(Session):
    def __init__(self,platform, channel_id, self_id) -> None:
        body = {
            'platform':platform,
            'guild':{
                'id':channel_id
            },
            'self_id':self_id
        }
        super().__init__(body)

class User:
    def __init__(self, user_info):
        self.id = user_info.get('id')
        self.name = user_info.get('name')
        self.avatar = user_info.get('avatar')


class Channel:
    def __init__(self, channel_info):
        self.type = channel_info.get('type')
        self.id = channel_info.get('id')
        self.name = channel_info.get('name')


class Guild:
    def __init__(self, guild_info):
        self.id = guild_info.get('id')
        self.name = guild_info.get('name')
        self.avatar = guild_info.get('avatar')


class Member:
    def __init__(self, guild_info):
        self.name = guild_info.get('name')


class Message:
    def __init__(self, message_info):
        self.id = message_info.get('id')
        self.content = message_info.get('content')