import sys
import time
from functools import wraps

__doc__ = '''Tracer, on one hand, helps confirm the execution time and number of specified (all) functions; 
        on the other hand, it is used to display the time cost between specified lines. 
示踪器，一方面帮助确定指定（全部）函数执行时间与次数；另一方面用来显示某行执行时间。
Args:
custom: show custom(*args, **kwargs) after function Tracer string.
show_ms: show bits of ms.
callback: such as callback=lambda *a,**aa:print(time.time()), will instead of print default log.

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
    dd(b=1, c=2)
    time.sleep(0.387)
    dd(5)
test2()
# 2017-02-16 00:59:07 [ 00:00:00.000 ] | (dd) 1 args:() & kwargs:{} => None; Caller(test2, line: 156)  
# 2017-02-16 00:59:07 [ 00:00:00.469 ] | (dd) 2 args:() & kwargs:{'a': 3} => None; Caller(test2, line: 158)  
# 2017-02-16 00:59:07 [ 00:00:00.469 ] | (dd) 3 args:() & kwargs:{'b': 1, 'c': 2} => None; Caller(test2, line: 159)  
# 2017-02-16 00:59:08 [ 00:00:00.856 ] | (dd) 4 args:(5,) & kwargs:{} => None; Caller(test2, line: 161)  

# ----------------------------
# example 3: # Trace all functions
def aa(a): return 'a'
def cc(): return 'c'
def dd(): return 'd'
Tracer(custom=lambda x:'show func_name %s'%x.__name__).trace_all()
dd()
time.sleep(0.4687)
aa(['33'])
time.sleep(0.387)
cc()
time.sleep(0.387)
aa(2)
# 2017-02-16 01:00:23 [ 00:00:00.000 ] | (dd) 1 args:() & kwargs:{} => d; Caller(<module>, line: 150) show func_name dd 
# 2017-02-16 01:00:24 [ 00:00:00.469 ] | (aa) 1 args:() & kwargs:{} => a; Caller(<module>, line: 152) show func_name aa 
# 2017-02-16 01:00:24 [ 00:00:00.856 ] | (cc) 1 args:() & kwargs:{} => c; Caller(<module>, line: 154) show func_name cc 
# 2017-02-16 01:00:25 [ 00:00:01.255 ] | (aa) 2 args:() & kwargs:{} => a; Caller(<module>, line: 156) show func_name aa 

'''


class Tracer(object):

    """
Tracer, on one hand, helps confirm the execution time and number of specified (all) functions; 
on the other hand, it is used to display the time cost between specified lines. 
示踪器，一方面帮助确定指定（全部）函数执行时间与次数；另一方面用来显示某行执行时间。
Args:
custom: show custom(*args, **kwargs) after function Tracer string.
show_ms: show bits of ms.
callback: such as callback=lambda *a,**aa:print(time.time()), will instead of print default log.

Read more from model __doc__.

    """

    def __init__(self, custom=None, show_ms=3, callback=None):
        self.custom = custom or self.nothing
        self.start_time = time.time()
        self.last_call = 0
        self.show_ms = show_ms
        self.callback = callback

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
            ms = str(t).split('.')[1][:self.show_ms].rjust(
                3, '0') if '.' in str(t) else '000'
            return time.strftime("%H:%M:%S", time.gmtime(t))+'.%s' % ms
        if hasattr(f, '__call__'):
            count = 0

            @wraps(f)
            def d(*args, **kwargs):
                if self.callback:
                    self.callback(*args, **kwargs)
                else:
                    nonlocal count
                    count += 1
                    # print(f.__name__)
                    passed = trans_ms(time.time()-self.start_time)
                    now_readable = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime((time.time())))
                    result = f(*args, **kwargs)
                    print('%s [ %+6s ] | %s (%s) args:%s & kwargs:%s => %s; Caller(%s, line: %s) %s ' %
                          (now_readable, passed, f.__name__, count, args, kwargs,
                           repr(result), sys._getframe(1).f_code.co_name,
                           sys._getframe(1).f_lineno, self.custom(f)))
                return result
            return d
        else:
            if self.callback:
                return self.callback()
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
                return 'ok'
