import json


class Config:
    def __init__(self) -> None:
        self.config = json.load(open('config.json'))
    def getConfig(self):
        return self.config
    def getPort(self):
        return self.config.get('port','5500')
    def getHost(self):
        return self.config.get('host','localhost')
    def getToken(self):
        return self.config.get('token','')
    def getHeartbeatCd(self):
        return self.config.get('heart_beat_cd',60)