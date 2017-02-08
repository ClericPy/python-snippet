
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


def ttime(rawtime=None, tzone=8*3600, fail=''):
    '''
Translate timestamp into %Y-%m-%d %H:%M:%S. 时间戳转人类可读。
rawtime: if not set, use time.time(). support 10/13 bit int/float/str timestamp.
tzone: time zone, east eight time zone by default.
fail: while raise an error, return fail.
# example:
print(ttime())
print(ttime(1486572818.4218583298472936253)) # 2017-02-09 00:53:38
    '''
    import time
    try:
        rawtime = time.time() if rawtime is None else rawtime
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(str(rawtime)[:10])+time.timezone+tzone))
    except:
        return fail

# =========================================================================


class Slicer(object):

    """
Slicer, the sequence can be divided into a piece of the generator, can be cut by length, can be divided by the number of shares, can index/slice a generator also. 
切片器，将序列切分为一块一块的生成器，可以按长度切，可以按份数平分，可以对生成器索引/切片。
self.seq = iter(seq) # seq can be range, list, tuple, generator, iterator, file; as can be iter()
self.size = size # means use slice_by_size, slice seq 
self.filling = filling # when seq length can not be evenly divisible by size, fill with it
self.piece = piece # means use slice_by_piece
self.start_from = start_from # log/print the count has been done
self.log_func = log_func # print function
WARNING: one Slicer instance can't be used twice for the generator is `disposable`.
====================
Input: sequence
Output: iterator
- Example 1: 
print(list(Slicer(range(30))[4:15:2])) 
# [4, 6, 8, 10, 12, 14, 16]
# -------------------------
ss = Slicer(range(1000))
print(*ss[3:5])
# 3 4 5
print(*ss[3:5])
# 9 10 11
- Example 2: 
for i in Slicer(range(5),size=3,filling=0 ):print(i)
# (0, 1, 2)
# (3, 4, 0)
- Example 3: 
for i in Slicer(range(5),piece=2,filling=0 ):print(i)
# [0, 1]
# [2, 3, 4]
====================

    """

    def __init__(self, seq, size=None, piece=None, start_from=None, filling=None, log_func=print):
        self.seq = iter(seq)
        self.size = size
        self.filling = filling
        self.piece = piece
        self.start_from = start_from
        self.log_func = log_func
        if size is not None:
            self.generator = self.slice_by_size()
        elif piece is not None:
            self.generator = self.slice_by_piece()
        else:
            self.generator = self.seq

    def __next__(self):
        '''Implement next(self). For it's a generator.'''
        for item in self.generator:
            yield item

    def __iter__(self):
        '''Implement iter(self). Usually be used for `for` loop.'''
        return self.generator

    def __contains__(self, key):
        '''Return key in self. Sometimes maybe not work.'''
        return key in self.seq

    def __getitem__(self, x):
        '''Return self[key] or self[start:stop:step]'''
        if isinstance(x, slice):
            return self.slice(x.start, x.stop, x.step)
        if isinstance(x, int):
            it = self.new_range()
            nexti = next(it)
            for i, element in enumerate(self.seq):
                if i == nexti:
                    return element
                nexti = next(it)

    def close(self):
        raise GeneratorExit

    def send(self, arg):
        self.seq.send(arg)

    def slice(self, start=0, stop=None, step=None):
        '''Same as itertools.islice(iterable, start, stop[, step])'''
        stop = stop or float('inf')
        step = step or 1
        it = self.new_range(start, stop, step)
        nexti = next(it)
        for i, element in enumerate(self.seq):
            if i == nexti:
                yield element
                nexti = next(it)

    def itertools_chain(self, *iterables):
        '''From itertools import chain.'''
        for it in iterables:
            for element in it:
                yield element

    def new_range(self, start=0, stop=None, step=None):
        '''Similar to range, stop can be int'''
        step = step or 1
        stop = stop or float('inf')
        n = start-step
        while n < stop:
            n += step
            yield n

    def slice_by_piece(self):
        '''Equal division self.seq into self.piece pieces,
        merge the last two if self.seq'length is not evenly divisible by self.piece.'''
        seq_list = list(self.seq)
        seq_list_length = len(seq_list)
        size = seq_list_length//self.piece
        chunk_list = [seq_list[i:i+size] for i in range(0, seq_list_length, size)]
        if len(chunk_list) != self.piece:
            extra = list(self.itertools_chain(*chunk_list[self.piece:]))
            chunk_list = chunk_list[:self.piece]
            chunk_list[-1] += extra
        if self.start_from is not None:
            index = -1
            for i in chunk_list:
                index += 1
                if index < self.start_from:
                    continue
                self.log_func(index)
                yield i
        else:
            for i in chunk_list:
                yield i

    def slice_by_size(self):
        '''Split self.seq into chunks, the length of each chunk will be equal to self.size, 
        filled by self.filling if self.seq'length is not evenly divisible by self.size.
        '''
        chunk_generator = iter(zip(*(self.itertools_chain(self.seq, [self.filling]*self.size),) * (self.size)))
        if self.start_from is not None:
            index = -1
            for i in chunk_generator:
                index += 1
                if index < self.start_from:
                    continue
                self.log_func(index)
                yield i
        else:
            for i in chunk_generator:
                yield i

# =========================================================================

import sys
import time
from functools import wraps


class Tracer(object):

    """
Tracer, on the one hand, helps confirm the execution time and number of specified (all) functions; on the other hand, it is used to display the time cost between specified lines. 
示踪器，一方面帮助确定指定（全部）函数执行时间与次数；另一方面用来显示某行执行时间。

import sys
import time
from functools import wraps

example 1: # Trace specified lines
ss = Tracer()
ss()
time.sleep(0.4687)
ss()
time.sleep(0.4687)
ss()
time.sleep(0.4687)
ss()
# 2017-02-09 02:32:57 [Interval, Passed: (   0ms /    0ms)] | Caller: <module> (line: 77)
# 2017-02-09 02:32:58 [Interval, Passed: ( 484ms /  484ms)] | Caller: <module> (line: 79)
# 2017-02-09 02:32:58 [Interval, Passed: ( 484ms /  968ms)] | Caller: <module> (line: 81)
# 2017-02-09 02:32:59 [Interval, Passed: ( 484ms / 1.453s)] | Caller: <module> (line: 83)
----------------------------
example 2: # Trace specified functions by decorator
tracer = Tracer()
@tracer
def dd(a=2):
    pass
dd()
time.sleep(0.4687)
dd()
dd()
time.sleep(0.387)
dd()
# 2017-02-09 02:35:20 [    0ms ] | Object: dd (1) 
# 2017-02-09 02:35:21 [  484ms ] | Object: dd (2) 
# 2017-02-09 02:35:21 [  484ms ] | Object: dd (3) 
# 2017-02-09 02:35:21 [  875ms ] | Object: dd (4) 
----------------------------
example 3: # Trace all functions
def aa(): pass
def cc(): pass
def dd(): pass
Tracer.trace_all()
dd()
time.sleep(0.4687)
aa()
cc()
time.sleep(0.387)
aa()
# 2017-02-09 02:38:42 [    0ms ] | Object: dd (1) 
# 2017-02-09 02:38:42 [  484ms ] | Object: aa (1) 
# 2017-02-09 02:38:42 [  484ms ] | Object: cc (1) 
# 2017-02-09 02:38:43 [  875ms ] | Object: aa (2) 

    """
    start_time = time.time()
    last_call = 0

    @classmethod
    def trace_all(cls):
        globals_dict = globals()
        funcs = [globals_dict[i] for i in globals_dict if hasattr(globals_dict[i], '__call__') and (i not in ['wraps', cls.__name__])]
        # [cls()]
        for i in funcs:
            globals()[i.__name__] = cls.__call__(i)

    @classmethod
    def __call__(cls, f=None):
        if hasattr(f, '__call__'):
            count = 0

            @wraps(f)
            def d(*args, **argvs):
                nonlocal count
                count += 1
                # print(f.__name__)
                passed = (time.time()-cls.start_time)
                passed = '%.3fs' % (passed) if passed > 1 else '%dms' % (passed*1000)
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((time.time())))
                print('%s [ %+6s ] | Object: %s (%s) ' % (now, passed, f.__name__, count))
                return f(*args, **argvs)
            return d
        else:
            def trans_ms(t):
                if t > 100000:
                    return t
                elif 1 < t < 100000:
                    t = '%.3fs' % (t)
                elif t < 1:
                    t = '%dms' % (t*1000)
                else:
                    t = '%ds' % (t)
                return t
            now = time.time()
            intervar = trans_ms(now-(cls.last_call or now))[:6]
            passed = trans_ms(now-cls.start_time)[:6]
            cls.last_call = now
            now_readable = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((now)))
            print('%s [Interval, Passed: (%+6s / %+6s)] | Caller: %s (line: %s)' % (now_readable, intervar, passed, sys._getframe(1).f_code.co_name, sys._getframe(1).f_lineno))
