# python-snippet 

### Install:

> version 0.0.2

> pip install py_snippets -U

## Situation for Usage

```python
from py_snippets import saver
print(saver.__doc__)
```

### 1. asyncme

> Same as [torequests](https://github.com/ClericPy/torequests) but without **tPool**.

* async any function / class (hasattr __call__)

```python
from py_snippets.asyncme import threads, Async, Pool
import time

# example 1: use Decorator threads to change any Function/Class asynchronous.

@threads(timeout=0.5, timeout_return=lambda *args, **kwargs: (args, kwargs))
def test1(*args, **kwargs):
    time.sleep(1)
    print(
        'TimeoutError, but future is still running...'
        ' so do not define a non-stop function!!!')
    return 100

result = test1(1, 2, 3, 5, a=100, b=1000)
print('here is one future instance: ', result)
print(result.x)
# here is one future instance:  <NewFuture at 0x2f9a750 state=running>
# ((1, 2, 3, 5), {'a': 100, 'b': 1000})
# TimeoutError, but future is still running... so do not define a non-stop
# function

# example 2: if you don't want to modify raw function, use Async.


def test2(arg):
    time.sleep(arg)
    return arg

async_test2 = Async(test2, timeout=1.0, timeout_return=lambda x: 'bad %s' % x)
futures = [async_test2(i) for i in (1, 2, 3, 5)]  # not blocked
print('here is one future instance: ', futures[0], 111)
# here is one future instance:  <NewFuture at 0x35916d0 state=running>
results = [i.x for i in futures]  # will cost 5s, not 1s
print(results)  # [1, 'bad 2', 'bad 3', 'bad 5']
```
### 2. init_logger

> initial logger easily. for log file or stdout.

```python
from py_snippets.init_logger import init_logger

# example:
def test():
    # logger = init_logger() # default config for command line INFO logger.
    logger = init_logger(handlers=[['', 'info'],['error.log','error'],['custom.log',21]])
    logger.info('info')
    logger.error('error')
test()
# stdout:
# INFO      [2017-03-03 00:40:59]  unnamed (test: 7): ss
# ERROR     [2017-03-03 00:40:59]  unnamed (test: 8): ss
# file error.log & custom.log:
# ERROR     [2017-03-03 00:42:12]  unnamed (test: 8): error
```
### 3. progress_bar

> simple progress_bar tool for iters.

```python
from py_snippets.progress_bar import progress_bar
import time
# examples:
# run in command line, all progress_bar show in one line without newline.
for item in progress_bar(range(10),1,1,1,30):
    time.sleep(.5)
    do_sth = item 
# ■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□ 30.0% (-7)
```
### 4. retry

> simple retry tool for functions.

```python
from py_snippets.retry import retry

# example:
@retry(1,0,1)
def test(a=3):
    a/0 
    pass

test()
# 2017-03-03 00:56:00 | Object: test (retry: 0) args:() ; kwargs:{}; error: division by zero;
# 2017-03-03 00:56:00 | Object: test (retry: 1) args:() ; kwargs:{}; error: division by zero;
```

### 5. saver

> save args for persistence.

```python
from py_snippets.saver import Saver
db = Saver() # path maybe default not set

# it's easy use but slowwwwwwww
for i in range(5):
    db[str(i)] = i

# it's for massive keys, fast
db.update({'a':'a'})
db.update(**{'b':'b'})

print(db.keys())
# {'a', '2', '4', '1', 'b', '3', '0'}
print(db.items())
# {('0', 0), ('4', 4), ('b', 'b'), ('3', 3), ('1', 1), ('a', 'a'), ('2', 2)}
print(db.values())
# [0, 1, 2, 3, 4, 'a', 'b']
print(len(db), db.pop('4'), len(db))
# 7 4 6
print(len(db), db.popitem(), len(db))
# 6 ('0', 0) 5
print(db.info)
# {'keys': 5, 'file_size': '3.0 KB'}
# db.clear() # will delete all files
```

### 5. slicer

> the sequence can be divided into a piece of the generator, can be cut by length, 
can be divided by the number of shares, can index/slice a generator also. 

```python
from py_snippets.slicer import Slicer
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
# Example 5:
print(list(Slicer(([1,2],[1,2,3,4],[1,4,2],[1,3,2]),unique_key=lambda x:x[-1])))
print(list(Slicer((3,1,2,3,1,2,3)).unique()))
# [[1, 2], [1, 2, 3, 4]]
# [3, 1, 2]
```
### 6. times

> read timestamp

```python
from py_snippets.times import Times
tt = Times()
print(tt.ttime()) # 2017-02-14 00:34:11
print(tt.timeago()) # 47 年 1 月 25 天 16 小时 34 分钟 11 秒
print(tt.timeago(start=-3, lang='')) # 16 hours 34 mins 11 s
```

### 7. tracer

> Tracer, on one hand, helps confirm the execution time and number of specified (all) functions; 
        on the other hand, it is used to display the time cost between specified lines. 
        
```python
from py_snippets.tracer import Tracer

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
```

