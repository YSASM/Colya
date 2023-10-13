import json
import logging
import re

import requests
from Colya.Config.config import Config
from Colya.utils.utils import async_call,msgFormat
from Colya.plugin.loadPlugin import Loader
class MessageService:
    def __init__(self) -> None:
        self.pluginLoader = Loader()
        self.pluginLoader.load()
    @async_call
    def receive(self,msg):
        # data = json.loads(message)
        # 这里直接unescape_special_characters可能会导致混淆
        data = json.loads(msgFormat(msg))
        # print("Dev中信息：", data)
        if data['op'] == 4:
            platform = data['body']['logins'][0]['platform']
            bot_name = data['body']['logins'][0]['user']['name']
            logging.info(f"Satori驱动器连接成功，{bot_name} 已上线 [{platform}] ！")
        elif data['op'] == 0:
            session = Session(data["body"])
            self.pluginLoader.matchMsgPlugin(session)
            user_id = session.user.id
            try:
                member = session.user.name
                if not member:
                    member = f'QQ用户{user_id}'
            except:
                # 为什么是QQ用户，因为就QQ可能拿不到成员name...
                member = f'QQ用户{user_id}'
            content = f"[{'群组消息:'+str(session.guild.name)+'|'+member if session.isGroupMsg else '私聊消息:'+member}]"+session.message.content
            # logging.info(( {member} )" + session.message.content)
            logging.info(content)
        elif data['op'] == 2:
            # print('[心跳状态：存活]')
            pass




class Session:
    def __init__(self, body):
        self.id = body.get('id')
        self.type = body.get('type')
        self.platform = body.get('platform')
        self.self_id = body.get('self_id')
        self.timestamp = body.get('timestamp')
        self.user = User(body.get('user', {}))
        self.channel = Channel(body.get('channel', {}))
        self.guild = Guild(body.get('guild', {}))
        self.member = body.get('member', {})
        self.message = Message(body.get('message', {}))
        self.isGroupMsg = self.guild.name != None

class setMsgSession(Session):
    def __init__(self,platform, channel_id, self_id) -> None:
        body = {
            'platform':platform,
            'guild':{
                'id':channel_id
            },
            'self_id':self_id
        }
        super().__init__(self,body)

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


class SendMessage:
    def __init__(self,session:Session) -> None:
        self.session = session
        self.config = Config()
    
    def send_string(self,string):
        """
        发送消息到指定频道。
        Parameters:
        string (str): 消息内容。
        Returns:
        dict: 包含消息信息的字典，如果发送失败则返回None。
        """
        # API endpoint

        endpoint = f'http://{self.config.getHost()}:{self.config.getPort()}/v1/message.create'  # 替换为实际API endpoint

        # 构建请求参数
        request_data = {
            'channel_id': self.session.guild.id,
            'content': string
        }

        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.getToken()}',
            'X-Platform': self.session.platform,
            'X-Self-ID': self.session.self_id
        }

        # 发送POST请求
        # response = requests.post(endpoint, data=json.dumps(request_data), headers=headers)
        response = requests.post(endpoint, data=json.dumps(request_data), headers=headers, verify=True)

        # 检查响应
        if response.status_code == 200:
            # 解析响应为JSON格式
            response_data = response.json()
            return response_data
        else:
            print('Failed to create message. Status code:', response.status_code)
            return None
