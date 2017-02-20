import time

__doc__ = '''# examples:
tt = Times()
print(tt.ttime())
print(tt.timeago())
print(tt.timeago(start=-3, lang=''))
# 2017-02-14 00:34:11
# 47 年 1 月 25 天 16 小时 34 分钟 11 秒
# 16 hours 34 mins 11 s
'''


class Times(object):

    """# examples:
tt = Times()
print(tt.ttime())
print(tt.timeago())
print(tt.timeago(start=-3, lang=''))
# 2017-02-14 00:34:11
# 47 年 1 月 25 天 16 小时 34 分钟 11 秒
# 16 hours 34 mins 11 s

Read more from model __doc__.

 """

    def __init__(self, rawtime=None):
        self.rawtime = int(str(rawtime or time.time())[:10])

    def ttime(self, tzone=8*3600, fail=''):
        '''
    Translate timestamp into %Y-%m-%d %H:%M:%S. 时间戳转人类可读。
    tzone: time zone, east eight time zone by default.
    fail: while raise an error, return fail.
    # example:
    print(ttime())
    print(ttime(1486572818.4218583298472936253)) # 2017-02-09 00:53:38
        '''
        try:
            rawtime = time.time() if self.rawtime is None else self.rawtime
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rawtime + time.timezone+tzone))
        except:
            return fail

    def timeago(self, start=0, end=6, lang='cn'):
        times = []
        rawtime = self.rawtime
        readable = ('年', '月', '天', '小时', '分钟', '秒') if lang == 'cn' else (
            'years', 'months', 'days', 'hours', 'mins', 's')
        if rawtime == 0:
            return '0 秒'
        for i in zip((31536000, 2592000, 86400, 3600, 60, 1), readable):
            new = rawtime//i[0]
            if new:
                times.append('%s %s' % (new, i[1]))
            rawtime = rawtime - new*i[0]
        return ' '.join(times[start:end])
