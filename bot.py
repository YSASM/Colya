import asyncio
from Colya.service.WebSocket import WebSocket

class Bot:
    def __init__(self) -> None:
        self.wb = WebSocket()
        
    def run(self):
        
        asyncio.get_event_loop().run_until_complete(self.wb.connect())