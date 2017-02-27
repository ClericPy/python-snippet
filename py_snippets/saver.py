import time

__doc__ = '''
    name: set None to use variable name dynamically; or set a name with str.
    db: shelve(non-cross-platform:built-ins), sqiltedict(thread-safe:good)
    path: db file path.
    One Saver instance use same file path
    # example 1:
        ss = Saver()
        d = 'ddd'
        ss.x = d
        a= 'aaa'
        ss.x = a
        ss.show()
        # {'a': 'aaa', 'd': 'ddd'}
        # ss.delete()
    # example 2:
        ss = Saver('same_name')
        d = {'ddd':333}
        ss.x = d
        a= {'aaa':345}
        ss.x = a
        ss.show()
        # {'same_name': 'aaa'}
        reuse = ss.x
        print(reuse)
'''


class Saver(object):

    """
    name: set None to use variable name dynamically; or set a name with str.
    db: shelve(non-cross-platform:built-ins), sqiltedict(thread-safe:good)
    path: db file path.
    One Saver instance use same file path
    """

    def __init__(self, name=None, db='shelve', path=None):
        super(Saver, self).__init__()
        self.name = name
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

    def extract_name(self, obj):
        import sys
        probable_name = [key for key, value in sys._getframe(
            1).f_back.f_locals.items() if value is obj]
        if len(probable_name) == 1:
            return probable_name[0]
        else:
            print(probable_name, 'invalid name')
            raise BaseException('obj should be unique for finding arg name')

    def delete(self):
        import os
        for fn in self.db_files:
            try:
                os.remove(fn)
            except:
                pass

    def shutdown(self):
        self.delete()

    def clear(self):
        with self.db_open(self.path) as s:
            s.clear()

    def __dict__(self):
        with self.db_open(self.path) as s:
            return dict(s)

    def show(self):
        print(self.__dict__())

    def get(self, name, fail=None):
        with db_open(self.path) as s:
            return s[name] if name in s else fail

    @property
    def x(self):
        if not self.name:
            raise KeyError('Use self.get while name is None')
        return self.get(self.name)

    @x.setter
    def x(self, value):
        name = self.name or self.extract_name(value)
        with self.db_open(self.path) as s:
            s[name] = value
            self.db_commit(s)

    @x.deleter
    def x(self, value):
        name = self.name or self.extract_name(value)
        with self.db_open(self.path) as s:
            del s[name]
            self.db_commit(s)
