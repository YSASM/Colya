from threading import Thread

def msgFormat(msg):
    # 将转义字符替换回特殊字符
    msg = msg.replace('&quot;', '"')
    msg = msg.replace('&amp;', '&')
    msg = msg.replace('&lt;', '<')
    msg = msg.replace('&gt;', '>')
    return msg

def async_call(fn):
    def wrapper(*args, **kwargs):
        th = Thread(target=fn, args=args, kwargs=kwargs)
        th.setDaemon(True)
        th.start()
    return wrapper