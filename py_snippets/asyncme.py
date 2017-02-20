from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from concurrent.futures._base import Future
from concurrent.futures.thread import _WorkItem
from functools import wraps
import time

__doc__ = '''
Asnyc/threads: make any Function/Class asynchronous.
异步函数、异步修饰器：使任意一个函数或者类这种带有__call__的成为异步的
Args:
    f : Async the function object, f.
    n=None: (os.cpu_count() or 1) * 5, The maximum number of threads that can be used to
            execute the given calls.
    timeout=None: Future.x will wait for `timeout` seconds for the function's result, 
            or return timeout_return(*args, **kwargs).
            WARN: Future thread will not stop running until function finished or pid killed.
    timeout_return=None: Call Future.x after timeout,
            if timeout_return is not true, return 'TimeoutError: %s, %s' % (self._args, self._kwargs)
            if timeout_return has __call__ attr, return timeout_return(*args, **kwargs)
            otherwise, return timeout_return itself.



# example 1: use Decorator threads to change any Function/Class asynchronous.
@threads(timeout=0.5, timeout_return=lambda *args, **kwargs: (args, kwargs))
def test1(*args, **kwargs):
    time.sleep(1)
    print(
        'TimeoutError, but future is still running...' \
        ' so do not define a non-stop function')
    return 100

result = test1(1, 2, 3, 5, a=100, b=1000)
print('here is one future instance: ', result)
print(result.x)
# here is one future instance:  <NewFuture at 0x2f9a750 state=running>
# ((1, 2, 3, 5), {'a': 100, 'b': 1000})
# TimeoutError, but future is still running... so do not define a non-stop function

# example 2: if you don't want to modify raw function, use Async.

def test2(*args, **kwargs):
    time.sleep(1)
    return 100

async_test2 = Async(test2)
result = async_test2(1, 2, 3, 5, a=100, b=1000)
print('here is one future instance: ', result)
print(result.x)
# here is one future instance:  <NewFuture at 0x35916d0 state=running>
# 100
'''


class Pool(ThreadPoolExecutor):

    '''timeout_return while .x called but timeout.'''

    def __init__(self, n=None, timeout=None, timeout_return=None):
        super(Pool, self).__init__(n)
        self.timeout = timeout
        self.timeout_return = timeout_return

    def async_func(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return self.submit(f, *args, **kwargs)
        return wrapped

    def close(self,wait=True):
        self.shutdown(wait=wait)

    def submit(self, func, *args, **kwargs):
        '''self.submit(function,arg1,arg2,arg3=3)'''
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError(
                    'cannot schedule new futures after shutdown')
            future = NewFuture(
                self.timeout, self.timeout_return, args, kwargs)
            w = _WorkItem(future, func, args, kwargs)
            self._work_queue.put(w)
            self._adjust_thread_count()
            return future


class NewFuture(Future):

    """add .x (property) and timeout/timeout_return args for original Future
    timeout_return function only can be called while .x attribute called and raise TimeoutError.
    WARNING: Future thread will not stop running until function finished or pid killed.
    """

    def __init__(self, timeout=None, timeout_return=None, args=(), kwargs={}):
        super(NewFuture, self).__init__()
        self._timeout = timeout
        self._timeout_return = timeout_return
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, name):
        result = self.result(self._timeout)
        return result.__getattribute__(name)

    @property
    def x(self):
        try:
            return self.result(self._timeout)
        except TimeoutError:
            if not self._timeout_return:
                return 'TimeoutError: %s, %s' % (self._args, self._kwargs)
            if hasattr(self._timeout_return, '__call__'):
                return self._timeout_return(*self._args, **self._kwargs)
            return self._timeout_return


def Async(f, n=None, timeout=None, timeout_return=None):
    '''Here "Async" is not a class object, upper "A" only be used to differ
        from keyword "async" since python3.5+.
        Args:
        f : Async the function object, f.
        n=None: (os.cpu_count() or 1) * 5, The maximum number of threads that 
            can be used to execute the given calls.
        timeout=None: Future.x will wait for `timeout` seconds for the function's 
            result,  or return timeout_return(*args, **kwargs). 
            WARN: Future thread will not stop running until function finished or pid killed.
        timeout_return=None: Call Future.x after timeout, if timeout_return is 
            not true, return 'TimeoutError: %s, %s' % (self._args, self._kwargs) if timeout_return has __call__ attr, return timeout_return(*args, **kwargs) otherwise, return timeout_return itself.
'''
    return Pool(n, timeout, timeout_return).async_func(f)


def threads(n=None, timeout=None, timeout_return=None):
    '''Args:
        f : Async the function object, f.
        n=None: (os.cpu_count() or 1) * 5, The maximum number of threads that can be used to execute the given calls.
        timeout=None: Future.x will wait for `timeout` seconds for the function's result,  or return timeout_return(*args, **kwargs). WARN: Future thread will not stop running until function finished or pid killed.
        timeout_return=None: Call Future.x after timeout, if timeout_return is not true, return 'TimeoutError: %s, %s' % (self._args, self._kwargs) if timeout_return has __call__ attr, return timeout_return(*args, **kwargs) otherwise, return timeout_return itself.
'''
    return Pool(n, timeout, timeout_return).async_func


def get_by_time(new_futures, timeout=None):
    '''Return as a generator'''
    try:
        for i in as_completed(new_futures, timeout=timeout):
            yield i.x
    except Exception as e:
        yield e
