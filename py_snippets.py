#! not fit python2.x now

import logging


def init_logger(log_name=__file__, handlers=None, level=1, formatter=None,
                formatter_str=None):
    '''

log_name = 'my logger'
handlers = [['loggerfile.log',13],['','DEBUG'],['','info'],['','notSet']] # [[path,level]]
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
    levels = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
              'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
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
        handler = logging.FileHandler(
            path) if path else logging.StreamHandler()
        handler.setLevel(levels.get(handler_level.upper(), 1) if isinstance(
            handler_level, str) else handler_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# =========================================================================


import sys


def progress_bar(items='', inline=False, percent=False, left=False,
                 progress_bar_size=30):
    '''
 Progress bar 
 进度条
- items: one iterator, used for loop and yield one by one.
- inline: while running in command line, all progress_bar show in one line without newline.
  Lose effect for print/sys.stderr/sys.stdout. 
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
    length = len(items)
    for x, item in enumerate(items, 1):
        process = ''
        if progress_bar_size:
            done = int(x*progress_bar_size/length)
            todo = progress_bar_size-done
            process = '%s%s' % ('■'*done, '□'*todo)
        msg = '%s %s%%' % (process, round(
            x*100/length, 2)) if percent else '%s %s / %s' % (process, x, length)
        left_msg = ' (-%s)' % (length-x) if left else ''
        msg = '%s%s%s' % (
            msg, left_msg, '\r'*len(msg)) if inline else '%s\n' % msg
        sys.stderr.write(msg)
        yield item
    sys.stderr.write('\n\n')

# =========================================================================

import time


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
    try:
        rawtime = time.time() if rawtime is None else rawtime
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(str(rawtime)[:10])
                                                                 + time.timezone+tzone))
    except:
        return fail

# =========================================================================


class Slicer(object):

    """
Slicer, the sequence can be divided into a piece of the generator, can be cut by length, 
can be divided by the number of shares, can index/slice a generator also. 
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
# Example 1: 
print(list(Slicer(range(30))[4:15:2])) 
# [4, 6, 8, 10, 12, 14, 16]
# -------------------------
ss = Slicer(range(1000))
print(*ss[3:5])
# 3 4 5
print(*ss[3:5])
# 9 10 11
# Example 2: 
for i in Slicer(range(5),size=3,filling=0):print(i)
# (0, 1, 2)
# (3, 4, 0)
# Example 3: 
for i in Slicer(range(5),piece=2):print(i)
# [0, 1]
# [2, 3, 4]
# Example 4:
print(*Slicer(range(9), grams=5))
# (0, 1, 2, 3, 4) (1, 2, 3, 4, 5) (2, 3, 4, 5, 6) (3, 4, 5, 6, 7) (4, 5, 6, 7, 8)
====================

    """

    def __init__(self, seq, size=None, piece=None, start_from=None,
                 filling=None, grams=None, log_func=print):
        self.seq = iter(seq)
        self.size = size
        self.filling = filling
        self.piece = piece
        self.start_from = start_from
        self.log_func = log_func
        self.grams = grams
        if size is not None:
            self.generator = self.slice_by_size()
        elif piece is not None:
            self.generator = self.slice_by_piece()
        elif grams is not None:
            self.seq = tuple(seq)
            self.generator = self.n_grams()
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
            return self.islice(x.start or 0, x.stop, x.step)
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

    def n_grams(self):
        z = (self.islice(i) for i in range(self.grams))
        yield from zip(*z)
        # for i in (zip(*z)):
        # yield i

    def islice(self, start=0, stop=None, step=None):
        '''Same as itertools.islice(iterable, start, stop[, step])'''
        it = self.new_range(start, stop or float('inf'), step or 1)
        try:
            nexti = next(it)
        except StopIteration:
            return
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
        chunk_list = [seq_list[i:i+size]
                      for i in range(0, seq_list_length, size)]
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
            yield from chunk_list

    def slice_by_size(self):
        '''Split self.seq into chunks, the length of each chunk will be equal to self.size, 
        filled by self.filling if self.seq'length is not evenly divisible by self.size.
        '''
        chunk_generator = iter(
            zip(*(self.itertools_chain(self.seq, [self.filling]*self.size),) * (self.size)))
        if self.start_from is not None:
            index = -1
            for i in chunk_generator:
                index += 1
                if index < self.start_from:
                    continue
                self.log_func(index)
                yield i
        else:
            yield from chunk_generator


# =========================================================================

import sys
import time
from functools import wraps


class Tracer(object):

    """
Tracer, on the one hand, helps confirm the execution time and number of specified (all) functions; 
        on the other hand, it is used to display the time cost between specified lines. 
示踪器，一方面帮助确定指定（全部）函数执行时间与次数；另一方面用来显示某行执行时间。

import sys
import time
from functools import wraps

# example 1: # Trace specified lines
ss = Tracer()
def test():
    ss()
    time.sleep(0.4687)
    ss()
    time.sleep(0.4687)
    ss()
    time.sleep(0.4687)
    ss()
test()
# 2017-02-13 01:07:33 [Interval, Passed: (00:00:00.0 / 00:00:00.0)] | Caller: test (line: 466)
# 2017-02-13 01:07:33 [Interval, Passed: (00:00:00.469 / 00:00:00.469)] | Caller: test (line: 468)
# 2017-02-13 01:07:34 [Interval, Passed: (00:00:00.469 / 00:00:00.938)] | Caller: test (line: 470)
# 2017-02-13 01:07:34 [Interval, Passed: (00:00:00.469 / 00:00:01.407)] | Caller: test (line: 472)

# -----------------------------
# example 2: # Trace specified functions by decorator
tracer = Tracer()
@tracer
def dd(a=1, b=1, c=1):
    pass
def test2():
    dd()
    time.sleep(0.4687)
    dd(a=3)
    tracer()
    dd(b=1, c=2)
    time.sleep(0.387)
    dd(5)
test2()
# 2017-02-13 01:14:07 [ 00:00:00.0 ] | dd (1) args:() ; kwargs:{}; Caller(test2, line: 476)  
# 2017-02-13 01:14:07 [ 00:00:00.469 ] | dd (2) args:() ; kwargs:{'a': 3}; Caller(test2, line: 478)  
# 2017-02-13 01:14:07 [Interval, Passed: (00:00:00.0 / 00:00:00.469)] | Caller(test2, line: 479)
# 2017-02-13 01:14:07 [ 00:00:00.469 ] | dd (3) args:() ; kwargs:{'c': 2, 'b': 1}; Caller(test2, line: 480)  
# 2017-02-13 01:14:08 [ 00:00:00.856 ] | dd (4) args:(5,) ; kwargs:{}; Caller(test2, line: 482)  

# ----------------------------
# example 3: # Trace all functions
def aa(): pass
def cc(): pass
def dd(): pass
Tracer(custom=lambda x:'show func_name %s'%x.__name__).trace_all()
dd()
time.sleep(0.4687)
aa()
time.sleep(0.387)
cc()
time.sleep(0.387)
aa()
# 2017-02-13 01:06:11 [ 00:00:00.0 ] | Object: dd (1) args:() ; kwargs:{}; show func_name dd
# 2017-02-13 01:06:12 [ 00:00:00.469 ] | Object: aa (1) args:() ; kwargs:{}; show func_name aa
# 2017-02-13 01:06:12 [ 00:00:00.857 ] | Object: cc (1) args:() ; kwargs:{}; show func_name cc
# 2017-02-13 01:06:13 [ 00:00:01.244 ] | Object: aa (2) args:() ; kwargs:{}; show func_name aa


    """

    def __init__(self, custom=None, show_ms=3):
        self.custom = custom or self.nothing
        self.start_time = time.time()
        self.last_call = 0
        self.show_ms = show_ms

    def nothing(self, f):
        return ''

    def trace_all(self, ignore_names=['']):
        globals_dict = globals()
        funcs = [globals_dict[i] for i in globals_dict if
                 hasattr(globals_dict[i], '__call__') and
                 hasattr(globals_dict[i], '__name__') and
                 (i not in ['wraps', Tracer.__name__]+ignore_names)]
        tracer = Tracer(custom=self.custom, show_ms=self.show_ms)
        for i in funcs:
            globals()[i.__name__] = tracer.__call__(i)

    def __call__(self, f=None):
        def trans_ms(t):
            if t > 86400:
                return '%fs' % t
            ms = str(t).split('.')[1][
                :self.show_ms] if '.' in str(t) else '000'
            return time.strftime("%H:%M:%S", time.gmtime(t))+'.%s' % ms
        if hasattr(f, '__call__'):
            count = 0

            @wraps(f)
            def d(*args, **kwargs):
                nonlocal count
                count += 1
                # print(f.__name__)
                passed = trans_ms(time.time()-self.start_time)
                now_readable = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime((time.time())))
                print('%s [ %+6s ] | %s (%s) args:%s ; kwargs:%s; Caller(%s, line: %s) %s ' %
                      (now_readable, passed, f.__name__, count, args, kwargs,
                       sys._getframe(1).f_code.co_name,
                       sys._getframe(1).f_lineno, self.custom(f)))
                return f(*args, **kwargs)
            return d
        else:

            now = time.time()
            intervar = trans_ms(now-(self.last_call or now))
            passed = trans_ms(now-self.start_time)
            self.last_call = now
            now_readable = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime((now)))
            print('%s [Interval, Passed: (%+6s / %+6s)] | Caller(%s, line: %s)' %
                  (now_readable, intervar, passed, sys._getframe(1).f_code.co_name,
                   sys._getframe(1).f_lineno))

# =========================================================================


from functools import wraps


def retry(n=3, stop=False, log=False):
    '''
decorator for retrying
重试器（装饰器）
n: retry n times
stop: retry n times but still failed, then continue running if stop==False else raise Exception.
log: set it True will show log while retrying

- example:
@retry(1,0,1)
def test(a=3):
    a/0 
    pass

test()
# 2017-02-09 23:12:41 | Object: test (retry: 0) args:() ; kwargs:{}; error: division by zero;
# 2017-02-09 23:12:41 | Object: test (retry: 1) args:() ; kwargs:{}; error: division by zero;
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for _ in range(n+1):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    error = e
                    if log:
                        now_readable = time.strftime(
                            '%Y-%m-%d %H:%M:%S', time.localtime((time.time())))
                        print('%s | Object: %s (retry: %s) args:%s ; kwargs:%s; error: %s;' % (
                            now_readable, f.__name__, _, args, kwargs, error))
            else:
                if stop:
                    raise error
        return wrapper
    return decorator

# =========================================================================
