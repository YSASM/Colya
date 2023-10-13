import json
import logging
import re
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
class RanaUtils:
    @staticmethod
    def escape_special_characters(message):
        # 替换特殊字符为转义字符
        message = message.replace('"', '&quot;')
        message = message.replace('&', '&amp;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        return message

    @staticmethod
    def show_log(session):
        # 展示日志
        message_content = session.message.content

        html_tag_pattern = re.compile(r'<.*?>')
        # 将所有HTML标签替换为占位符
        cleaned_text = re.sub(html_tag_pattern, '[xml元素]', message_content)
        cleaned_text = cleaned_text[0:15] + '...' if len(cleaned_text) > 15 else cleaned_text

        user_id = session.user.id
        try:
            member = session.user.name
            if not member:
                member = f'QQ用户{user_id}'
        except:
            # 为什么是QQ用户，因为就QQ可能拿不到成员name...
            member = f'QQ用户{user_id}'
        print(f"[ {session.guild.name} ] （ {member} ）{cleaned_text}")


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


