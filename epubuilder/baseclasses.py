from collections import UserList, UserDict


class Limit:
    def add_before(self, index=None, key=None, item=None, obj=None):
        pass

    def add_after(self, index=None, key=None, item=None, obj=None):
        pass

    def del_before(self, index=None, key=None, item=None, obj=None):
        pass

    def del_after(self, index=None, key=None, item=None, obj=None):
        pass


class List(UserList):
    def __init__(self, initlist=None, limit=None, is_limit_when_init=True):
        self._limit = limit or Limit()
        initlist = initlist or []

        super().__init__()

        if initlist:
            if is_limit_when_init:
                self.data.extend(initlist)
            else:
                self.extend(initlist)

    def __setitem__(self, i, item):  # x[i] = item, del and add
        del self[i]
        self.insert(i, item)

    # all del item should be here
    def __delitem__(self, i):  # del x[i], del
        self._limit.del_before(index=i, obj=self)
        del self.data[i]
        self._limit.del_after(index=i, obj=self)

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add item should be here
    def insert(self, i, item):
        self._limit.add_before(index=i, item=item, obj=self)
        self.data.insert(i, item)
        self._limit.add_after(index=i, item=item, obj=self)

    def pop(self, i=-1):  # del
        x = self[i]
        del self[i]
        return x

    def remove(self, item):  # del
        i = self.index(item)
        del self[i]

    def clear(self):  # del
        for i in range(len(self)):
            self.pop()

    def extend(self, other):  # add
        for item in other:
            self.append(item)

    def __iadd__(self, other):  # x += y, add
        self.extend(other)
        return self

    def __imul__(self, n):  # x *= y, add
        old_data = self.copy()
        for x in range(n):
            self.extend(old_data)
        return self


class Dict(UserDict):
    def __init__(self, initdict=None, limit=None, is_limit_when_init=True):
        self._limit = limit or Limit()
        initdict = initdict or {}

        super().__init__()

        if initdict:
            if is_limit_when_init:
                self.data.update(initdict)
            else:
                self.update(initdict)

    # all set should be here
    def __setitem__(self, key, item):
        self._limit.add_before(key=key, item=item, obj=self)
        self.data[key] = item
        self._limit.add_after(key=key, item=item, obj=self)

    # all del should be here
    def __delitem__(self, key):
        self._limit.del_before(key=key, obj=self)
        del self.data[key]
        self._limit.del_after(key=key, obj=self)
