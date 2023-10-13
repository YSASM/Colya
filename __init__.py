import logging
import json
from logging import handlers
import os

if(not os.path.exists('log')):
    os.mkdir('log')

if(not os.path.exists('log/bot.log')):
    open('log/bot.log', "w").close()

if(not os.path.exists('plugin')):
    os.mkdir('plugin')

if(not os.path.exists('config.json')):
    open('config.json', "w").write(json.dumps({
        "host":"localhost",
        "port":"5500",
        "token":"",
        "heart_beat_cd":10
    })).close()
    logging.info("请填写config.json后再启动")
    exit(0)



logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
file_handler = handlers.TimedRotatingFileHandler(
    filename="log/bot.log", when="D", interval=1, backupCount=14
)
file_handler.setFormatter(logging.Formatter(fmt))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(console_handler)
logging.info("Colya启动中。。。")