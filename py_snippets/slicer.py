
__doc__ = '''Slicer, the sequence can be divided into a piece of the generator, can be cut by length, 
can be divided by the number of shares, can index/slice a generator also. 
切片器，将序列切分为一块一块的生成器，可以按长度切，可以按份数平分，可以对生成器索引/切片。
self.seq = iter(seq) # seq can be range, list, tuple, generator, iterator, file; as can be iter()
self.size = size # means use slice_by_size, slice seq 
self.filling = filling # when seq length can not be evenly divisible by size, fill with it
self.piece = piece # means use slice_by_piece
self.start_from = start_from # log/print the count has been done
self.log_func = log_func # print function
self.unique_key = unique_key # one function return the item unique key. (discard item with same key)
WARNING: one Slicer instance can't be used twice for the generator is `disposable`(not reusable).
====================
Input: sequence
Output: iterator
====================
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

====================
'''


class Slicer(object):

    """
self.seq = iter(seq) # seq can be range, list, tuple, generator, iterator, file; as can be iter()
self.size = size # means use slice_by_size, slice seq 
self.filling = filling # when seq length can not be evenly divisible by size, fill with it
self.piece = piece # means use slice_by_piece
self.start_from = start_from # log/print the count has been done
self.log_func = log_func # print function
self.unique_key = unique_key # one function return the item unique key. (discard item with same key)
WARNING: one Slicer instance can't be used twice for the generator is `disposable`(not reusable).

Read more from model __doc__.

 """

    def __init__(self, seq, size=None, piece=None, start_from=None,
                 filling=None, grams=None, unique_key=None, log_func=print):
        self.seq = iter(seq)
        self.size = size
        self.filling = filling
        self.piece = piece
        self.start_from = start_from
        self.grams = grams
        self.unique_key = unique_key
        self.log_func = log_func
        if size is not None:
            self.generator = self.slice_by_size()
        elif piece is not None:
            self.generator = self.slice_by_piece()
        elif grams is not None:
            self.seq = tuple(seq)
            self.generator = self.n_grams()
        elif unique_key is not None:
            self.generator = self.unique()
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

    def unique(self):
        '''Unique a sequence by source sorted, and discard item with same key.'''
        seen = set()
        for item in self.seq:
            val = item if self.unique_key is None else self.unique_key(item)
            if val not in seen:
                yield item
                seen.add(val)
