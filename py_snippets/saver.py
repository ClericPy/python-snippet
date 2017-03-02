import time

__doc__ = '''
    key: set None to use variable key dynamically; or set a key with str.
    db: shelve(non-cross-platform:built-ins), sqiltedict(thread-safe:good)
    path: db file path.
    One Saver instance use same file path
    # example 1:
        ss = Saver()
        d = 'ddd'
        ss.x = d
        a = 'aaa'
        ss.x = a
        def custom_func(arg):
            return arg
        ss.set('custom', custom_func)
        somewhere_custom = ss.get('custom')
        print(somewhere_custom)  # <function custom_func at 0x02E9B8E8>
        ss.show()
        # {'a': 'aaa', 'custom': <function custom_func at 0x030DB8E8>, 'd': 'ddd'}
        # ss.shutdown()
    # example 2:
        ss = Saver('same_key')
        d = {'ddd':333}
        ss.x = d
        a= {'aaa':345}
        ss.x = a
        ss.show()
        # {'same_key': 'aaa'}
        reuse = ss.x
        print(reuse)
'''


class Saver(object):

    """
    key: set None to use variable key dynamically; or set a key with str.
    db: shelve(non-cross-platform:built-ins), sqiltedict(thread-safe:good)
    path: db file path.
    One Saver instance use same file path
    """

    def __init__(self, key=None, db='shelve', path=None):
        super(Saver, self).__init__()
        self.key = key
        self.db = db
        self.path = path or 'saver_db'
        if db == 'shelve':
            import shelve
            self.db_open = shelve.open
            self.db_files = ['%s%s' % (self.path, ext)
                             for ext in ('', '.dat', '.bak', '.dir')]
            self.db_commit = lambda x: x.sync()
        if db == 'sqlitedict':
            import sqlitedict
            self.db_open = sqlitedict.SqliteDict
            self.db_files = [self.path] if self.path else []
            self.db_commit = lambda x: x.commit()

    def extract_key(self, obj):
        import sys
        probable_key = [v_name for v_name, value in sys._getframe(
            1).f_back.f_locals.items() if value is obj]
        if len(probable_key) == 1:
            return probable_key[0]
        else:
            print(probable_key, 'invalid key')
            raise BaseException('obj should be unique for finding arg name')

    def shutdown(self):
        import os
        for fn in self.db_files:
            try:
                os.remove(fn)
            except:
                pass

    def clear(self, remove=False):
        if remove:
            self.shutdown()
        with self.db_open(self.path) as s:
            s.clear()

    def __dict__(self):
        with self.db_open(self.path) as s:
            return dict(s)

    def show(self):
        print(self.__dict__())

    def get(self, key, fail=None):
        with self.db_open(self.path) as s:
            return s[key] if key in s else fail

    def set(self, key, value):
        with self.db_open(self.path) as s:
            s[key] = value
            self.db_commit(s)

    def delete(self, key):
        with self.db_open(self.path) as s:
            del s[key]
            self.db_commit(s)

    @property
    def x(self):
        if not self.key:
            raise KeyError('Use self.get while key is None')
        return self.get(self.key)

    @x.setter
    def x(self, value):
        key = self.key or self.extract_key(value)
        self.set(key, value)

    @x.deleter
    def x(self, value):
        key = self.key or self.extract_key(value)
        self.delete(key)
