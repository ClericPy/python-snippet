import time

__doc__ = '''# examples:
print(Times.ttime())
print(Times.ttime(0))
print(Times.timeago())
print(Times.timeago(start=-3, lang=''))
# 2017-03-25 00:17:04
# 1970-01-01 08:00:00
# 47 年 3 月 4 天 16 小时 17 分钟 4 秒
# 16 hours 17 mins 4 s

'''


class Times(object):

    """# examples:
print(Times.ttime())
print(Times.ttime(0))
print(Times.timeago())
print(Times.timeago(start=-3, lang=''))
# 2017-03-25 00:17:04
# 1970-01-01 08:00:00
# 47 年 3 月 4 天 16 小时 17 分钟 4 秒
# 16 hours 17 mins 4 s


Read more from model __doc__.

 """

    @staticmethod
    def ttime(timestamp=None, tzone=8*3600, fail=''):
        '''
    Translate timestamp into %Y-%m-%d %H:%M:%S. 时间戳转人类可读。
    tzone: time zone, east eight time zone by default.
    fail: while raise an error, return fail.
    # example:
    print(ttime())
    print(ttime(1486572818.4218583298472936253)) # 2017-02-09 00:53:38
        '''
        timestamp = timestamp if timestamp!=None else time.time()
        timestamp = int(str(timestamp).split('.')[0][:10])
        try:
            timestamp = time.time() if timestamp is None else timestamp
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp + time.timezone+tzone))
        except:
            return fail


    @staticmethod
    def timeago(seconds=None, start=0, end=6, lang='cn'):
        times = []
        seconds = seconds if seconds!=None else time.time()
        seconds = int(str(seconds).split('.')[0][:10])
        readable = ('年', '月', '天', '小时', '分钟', '秒') if lang == 'cn' else (
            'years', 'months', 'days', 'hours', 'mins', 's')
        if seconds == 0:
            return '0 秒'
        for i in zip((31536000, 2592000, 86400, 3600, 60, 1), readable):
            new = seconds//i[0]
            if new:
                times.append('%s %s' % (new, i[1]))
            seconds = seconds - new*i[0]
        return ' '.join(times[start:end])
