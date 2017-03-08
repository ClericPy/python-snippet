
__doc__ = '''
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

'''

class Saver(object):

    """
    Persistent dict.
    path: mode file path.
    mode: shelve(non-cross-platform:built-ins), sqiltedict(thread-safe:good)
    """

    def __init__(self, path='saver.db', mode=None):
        self.mode = mode
        self.path = path
        self.init_db()

    def init_db(self):
        if not self.mode:
            try:
                import sqlitedict
                self.mode = 'sqlitedict'
            except ImportError:
                print('sqlitedict not found, use shelve.')
                self.mode = 'shelve'
        if self.mode == 'sqlitedict':
            import sqlitedict
            self.db_open = sqlitedict.SqliteDict
            self.db_files = [self.path] if self.path else []
            self.db_commit = lambda x: x.commit()
            return
        if self.mode == 'shelve':
            import shelve
            self.db_open = shelve.open
            self.db_files = ['%s%s' % (self.path, ext)
                             for ext in ('', '.dat', '.bak', '.dir')]
            self.db_commit = lambda x: x.sync()
            return

        raise ImportError(
            'Invalid mode param, only support sqlitedict or shelve.')

    def extract_key(self, obj):
        import sys
        probable_key = [v_name for v_name, value in sys._getframe(
            1).f_back.f_locals.items() if value is obj]
        if len(probable_key) == 1:
            return probable_key[0]
        else:
            print(probable_key, 'invalid key')
            raise BaseException('obj should be unique for finding arg name')

    def __len__(self):
        return len(self.dict)

    def clear(self):
        self.shutdown()
        # with self.db_open(self.path) as s:
        #     s.clear()
        #     self.db_commit(s)
        # if self.mode == 'sqlitedict':
        #     import sqlite3
        #     conn = sqlite3.connect(self.path)
        #     conn.execute("VACUUM")
        #     conn.execute("VACUUM")
        #     conn.close()

    def keys(self):
        with self.db_open(self.path) as s:
            return set(s.keys())

    def items(self):
        with self.db_open(self.path) as s:
            return set(s.items())

    def values(self):
        with self.db_open(self.path) as s:
            return list(s.values())

    def pop(self, key):
        with self.db_open(self.path) as s:
            item = s.pop(key)
            self.db_commit(s)
            return item

    def popitem(self):
        with self.db_open(self.path) as s:
            item = s.popitem()
            self.db_commit(s)
            return item

    def __getitem__(self, key):
        with self.db_open(self.path) as s:
            if key in s:
                return s[key]
        raise KeyError

    def get(self, key, default=None):
        with self.db_open(self.path) as s:
            return s[key] if key in s else default

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        with self.db_open(self.path) as s:
            s[key] = value
            self.db_commit(s)

    def __delitem__(self, key):
        try:
            self.delete(key)
        except KeyError:
            print('not found key: %s' % key)

    def delete(self, key):
        with self.db_open(self.path) as s:
            del s[key]
            self.db_commit(s)

    def update(self, new_dict=None, **kwargs):
        new_dict = new_dict or {}
        with self.db_open(self.path) as s:
            s.update(new_dict)
            s.update(kwargs)
            self.db_commit(s)

    def shutdown(self):
        import os
        for fn in self.db_files:
            try:
                os.remove(fn)
            except:
                pass

    def __contains__(self, key):
        '''Return key in self. Sometimes maybe not work.'''
        with self.db_open(self.path) as s:
            if key in s:
                return True
            return False

    @property
    def dict(self):
        with self.db_open(self.path) as s:
            return dict(s)

    def __str__(self):
        '''return json.dumps'''
        import json
        return json.dumps(self.dict, ensure_ascii=False)

    @property
    def info(self):
        import os
        f_size = 0
        for fn in self.db_files:
            try:
                f_size += os.path.getsize(fn)
            except:
                pass
        info = {'file_size':'%s KB'%round(f_size/1024,2),'keys':len(self.keys())}
        return info