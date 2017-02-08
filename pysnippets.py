
def init_logger(log_name=__file__, handlers=None, level=1, formatter=None, formatter_str=None):
    '''

log_name = 'my logger'
handlers = [['loggerfile.log',13],['','DEBUG'],['','info'],['','notSet']] # [[path,level]]
formatter = logging.Formatter('%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s', "%Y-%m-%d %H:%M:%S")
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
    import logging

    levels = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
    if not formatter:
        if formatter_str:
            formatter_str = formatter_str
        else:
            formatter_str = '%(levelname)-8s  [%(asctime)s]  %(name)s (%(funcName)s: %(lineno)s): %(message)s'
        formatter = logging.Formatter(formatter_str, "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    handlers = handlers or [['', 'INFO']]

    # ---------------------------------------
    for each_handler in handlers:
        path, handler_level = each_handler
        handler = logging.FileHandler(path) if path else logging.StreamHandler()
        handler.setLevel(levels.get(handler_level.upper(), 1) if isinstance(handler_level, str) else handler_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# =========================================================================


def progress_bar(items='', inline=False, percent=False, left=False, progress_bar_size=30):
    '''
 Progress bar 
 进度条
- items: one iterator, used for loop and yield one by one.
- inline: while running in command line, all progress_bar show in one line without newline. Lose effect for print/sys.stderr/sys.stdout. 
- percent: show process by percent or counts/length.
- left: show number of not done.
- progress_bar_size: the length of progress_bar graph. Set less than screen width.

# examples:
import time
# run in command line, all progress_bar show in one line without newline.
for item in progress_bar(range(10),1,1,1,100):
    time.sleep(.5)
    do_sth = item # 

    '''
    import sys
    length = len(items)
    for x, item in enumerate(items, 1):
        process = ''
        if progress_bar_size:
            done = int(x*progress_bar_size/length)
            todo = progress_bar_size-done
            process = '%s%s' % ('■'*done, '□'*todo)
        msg = '%s %s%%' % (process, round(x*100/length, 2)) if percent else '%s %s / %s' % (process, x, length)
        left_msg = ' (-%s)' % (length-x) if left else ''
        msg = '%s%s%s' % (msg, left_msg, '\r'*len(msg)) if inline else '%s\n' % msg
        sys.stderr.write(msg)
        yield item
    sys.stderr.write('\n\n')

# =========================================================================



