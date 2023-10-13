import logging
from logging import handlers
import os

if(not os.path.exists('log')):
    os.mkdir('log')
if(not os.path.exists('log/bot.log')):
    open('log/bot.log', "w").close()

logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
file_handler = handlers.TimedRotatingFileHandler(
    filename="log/api.log", when="D", interval=1, backupCount=14
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