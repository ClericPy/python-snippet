from functools import wraps
import time
__doc__ = '''decorator for retrying
重试器（装饰器）
n: retry n times
stop: retry n times but still failed, then continue running if stop==False else raise Exception.
log: set it True will show log while retrying
callback: if callback is not None, will return callback(*args, **kwargs), for example: 
          callback=lambda *args, **kwargs:print(args, kwargs) .

- example:
@retry(1,0,1)
def test(a=3):
    a/0 
    pass

test()
# 2017-02-09 23:12:41 | Object: test (retry: 0) args:() ; kwargs:{}; error: division by zero;
# 2017-02-09 23:12:41 | Object: test (retry: 1) args:() ; kwargs:{}; error: division by zero;
'''


def retry(n=3, stop=False, log=False, callback=None):
    '''Args:
n: retry n times
stop: retry n times but still failed, then continue running if stop==False else raise Exception.
log: set it True will show log while retrying
callback: if callback is not None, will return callback(*args, **kwargs), for example: 
          callback=lambda *args, **kwargs:print(args, kwargs) .

Read more from model __doc__.

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
                if callback:
                    return callback(*args, **kwargs)
                if stop:
                    raise error
        return wrapper
    return decorator
