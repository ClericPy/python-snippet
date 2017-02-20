import logging

__doc__ = '''Args:
    log_name = 'unnamed'
    handlers = [['loggerfile.log',13],['','DEBUG'],['','info'],['','notSet']] # [[path,level]]
    level : the least level for the logger named log_name.
    formatter = logging.Formatter(
            '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s',
             "%Y-%m-%d %H:%M:%S")
    formatter_str = '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s'

# example:
def test():
    # logger = init_logger() # default config for command line INFO logger.
    logger = init_logger(handlers=[['', 'info'],['error.log','error'],['custom.log',21]])
    logger.info('ss')
    logger.error('ss')
test()

tips:
custom formatter:
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(created)f 当前时间，用UNIX标准的表示时间的浮点数表示
%(filename)s 调用日志输出函数的模块的文件名
%(funcName)s 调用日志输出函数的函数名
%(levelname)s 文本形式的日志级别
%(levelno)s 数字形式的日志级别
%(lineno)s 调用日志输出函数的语句所在的代码行
%(message)s 用户输出的消息
%(module)s  调用日志输出函数的模块名
%(name)s Logger的名字
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(process)s 进程ID。可能没有
%(relativeCreated)s 输出日志信息时的，自Logger创建以 来的毫秒数
%(thread)s 线程ID。可能没有
%(threadName)s 线程名。可能没有
    '''


def init_logger(log_name='unnamed', handlers=None, level=1, formatter=None,
                formatter_str=None):
    '''Args:
    log_name = 'unnamed'
    handlers = [['loggerfile.log',13],['','DEBUG'],['','info'],['','notSet']] # [[path,level]]
    level : the least level for the logger named log_name.
    formatter = logging.Formatter(
            '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s',
             "%Y-%m-%d %H:%M:%S")
    formatter_str = '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s'

Read more from model __doc__.


    '''
    levels = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
              'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
    if not formatter:
        if formatter_str:
            formatter_str = formatter_str
        else:
            formatter_str = '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s'
        formatter = logging.Formatter(formatter_str, "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(str(log_name))
    logger.setLevel(level)
    handlers = handlers or [['', 'INFO']]

    # ---------------------------------------
    for each_handler in handlers:
        path, handler_level = each_handler
        handler = logging.FileHandler(
            path) if path else logging.StreamHandler()
        handler.setLevel(levels.get(handler_level.upper(), 1) if isinstance(
            handler_level, str) else handler_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
