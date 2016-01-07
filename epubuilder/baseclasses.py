from collections import UserList, UserDict, UserString


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
        self.limits = []
        if limit:
            self.limits.append(limit)

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
        [limit.del_before(index=i, obj=self) for limit in self.limits]

        del self.data[i]

        [limit.add_after(index=i, obj=self) for limit in self.limits]

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add item should be here
    def insert(self, i, item):
        [limit.add_before(index=i, item=item, obj=self) for limit in self.limits]

        self.data.insert(i, item)

        [limit.add_after(index=i, item=item, obj=self) for limit in self.limits]

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
        self.limits = []
        if limit:
            self.limits.append(limit)

        initdict = initdict or {}

        super().__init__()

        if initdict:
            if is_limit_when_init:
                self.data.update(initdict)
            else:
                self.update(initdict)

    # all set should be here
    def __setitem__(self, key, item):

        [limit.add_before(key=key, item=item, obj=self) for limit in self.limits]

        self.data[key] = item

        [limit.add_after(key=key, item=item, obj=self) for limit in self.limits]

    # all del should be here
    def __delitem__(self, key):
        [limit.del_before(key=key, obj=self) for limit in self.limits]

        del self.data[key]

        [limit.del_after(key=key, obj=self) for limit in self.limits]


class Str(UserString):
    pass



