import asyncio
import json
import websockets
from Colya.Config.config  import Config
import logging
from .MessageService import MessageService

class WebSocket:
    def __init__(self):
        self.config = Config()
        self.websocket = None
        self.token = self.config.getToken()
        self.ws_url = f"ws://{self.config.getHost()}:{self.config.getPort()}/v1/events"
        self.msgservice = MessageService()
    
    async def connect(self):
        # 链接ws
        self.websocket = await websockets.connect(self.ws_url)
        if(not self.websocket):
            logging.error("websocket链接失败。。。。。。")
            return None
        logging.info("websocket链接成功,开始连接Satori服务。。。。。。")
        # 链接satori
        await self.websocket.send(json.dumps({
            "op": 3,
            "body": {
                "token": self.token,
                "sequence": None  # You may set a sequence if needed for session recovery
            }
        }))
        # 心跳测试
        asyncio.create_task(self._heart())
        # 开始接收消息
        while True:
            try:
                message = await self.websocket.recv()
                self.msgservice.receive(message)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed.")
                break
    async def _heart(self):
        await self.websocket.send(json.dumps({
            "op": 1,
            "body": {
                "美少女客服": "我是一只心跳猫猫"
            }
        }))
        await asyncio.sleep(self.config.getHeartbeatCd()) 