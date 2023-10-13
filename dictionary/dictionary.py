import json
import requests

from Colya.Config.config import Config


POST = 'post'
GET = 'get'

class Call:
    def __init__(self,method,url,data) -> None:
        self.config = Config()
        self.method = method
        self.url = url
        self.data = data
    
    def run(self):
        # API endpoint
        endpoint = f'http://{self.config.getHost()}:{self.config.getPort()}/v1{self.url}'  # 替换为实际API endpoint
        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.getToken()}',
            'X-Platform': self.session.platform,
            'X-Self-ID': self.session.self_id
        }

        response = requests.post(endpoint, json=self.data, headers=headers, verify=True)
        # 检查响应
        if response.status_code == 200:
            # 解析响应为JSON格式
            try:
                return response.json()
            except:
                return None
        else:
            return None


class _Base:
    def __init__(self,method,url, data) -> None:
        self.method = method
        self.url = url
        self.data = data
    def do(self):
        Call(self.method,self.url,self.data).run()


class Channel(_Base):
    '''
    频道 (Channel) 
    类型定义
    Channel
    :param id	        string	        频道 ID
    :param type	        Channel.Type	频道类型
    :param name	        string?	        频道名称
    :param parent_id	string?	        父频道 ID

    Channel.Type
    :param TEXT	0	文本频道
    :param VOICE	1	语音频道
    :param CATEGORY	2	分类频道
    :param DIRECT	3	私聊频道
    '''
    def __init__(self, method, url, data) -> None:
        self.baseUrl = '/channel'
        super().__init__(method, f'{self.baseUrl}.{url}',data)

class ChannelGet(Channel):
    '''
    获取群组频道
    :param channel_id	string	频道 ID

    根据 ID 获取频道。返回一个 Channel 对象。
    '''
    def __init__(self,data) -> None:
        super().__init__(POST,'get',data)
        
class ChannelList(Channel):
    '''
    获取群组频道列表
    :param guild_id	string	群组 ID
    :param next	string	分页令牌

    获取群组中的全部频道。返回一个 Channel 的 分页列表。
    '''
    def __init__(self,data) -> None:
        super().__init__(POST,'list',data)

class ChannelCreate(Channel):
    '''
    创建群组频道
    :param guild_id	string	群组 ID
    :param data	Channel	频道数据

    创建群组频道。返回一个 Channel 对象。
    '''
    def __init__(self,data) -> None:
        super().__init__(POST,'create',data)

class ChannelUpdate(Channel):
    '''
    修改群组频道
    :param channel_id	string	频道 ID
    :param data	Channel	频道数据

    修改群组频道。
    '''
    def __init__(self,data) -> None:
        super().__init__(POST,'update',data)    

class ChannelDelete(Channel):
    '''
    删除群组频道
    :param channel_id	string	频道 ID

    删除群组频道。
    '''
    def __init__(self,data) -> None:
        super().__init__(POST,'delete',data)    

class UserChannelCreate(Channel):
    '''
    创建私聊频道
    :param user_id	string	用户 ID

    创建一个私聊频道。返回一个 Channel 对象。
     '''
    def __init__(self,data) -> None:
        super().__init__(POST,'create',data) 
        self.url = self.url.replace('/','/user.')

class Guild(_Base):
    def __init__(self, method, url, data) -> None:
        self.baseUrl = '/guild'
        super().__init__(method, f'{self.baseUrl}.{url}',data)
