from collections import UserList, UserDict


class List(UserList):
    def __init__(self, initlist=None, before_add=None, after_add=None, before_del=None, after_del=None):
        super().__init__(initlist)
        # self.data = super(List, self).data

        self._before_add = before_add
        self._after_add = after_add
        self._before_del = before_del
        self._after_del = after_del

        if initlist:
            for item in initlist:
                if self._before_add:
                    self._before_add(item=item, obj=self)

                self.data.append(item)

                if self._after_add:
                    self._after_add(item=item, obj=self)

    def __setitem__(self, i, item):  # x[i] = item, del and add
        del self[i]
        self.insert(i, item)

    # all del item should be here
    def __delitem__(self, i):  # del x[i], del
        if self._before_del:
            self._before_del(index=i, obj=self)
        del self.data[i]

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add item should be here
    def insert(self, i, item):
        self._before_add and self._before_add(item=item, obj=self)
        self.data.insert(i, item)

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
    def __init__(self, before_set=None, after_set=None, before_del=None, after_del=None):
        super().__init__()
        self._before_set = before_set
        self._after_set = after_set
        self._before_del = before_del
        self._after_del = after_del

    # all set should be here
    def __setitem__(self, key, item):
        self._before_set and self._before_set(key=key, item=item)
        self.data[key] = item
        self._after_set and self._after_set(key=key, item=item)

    # all del should be here
    def __delitem__(self, key):
        self._before_del and self._before_del(key=key)
        del self.data[key]
        self._after_del and self._after_del(key=key)
