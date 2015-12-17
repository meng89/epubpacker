from collections import UserList


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

    def __contains__(self, item): return item in self.data

    def __len__(self): return len(self.data)

    def __getitem__(self, i): return self.data[i]

    def __setitem__(self, i, item):
        del self[i]
        self.insert(i, item)

    # all del item should be here
    def __delitem__(self, i):
        if self._before_del:
            self._before_del(index=i, obj=self)
        del self.data[i]

    def append(self, item):
        self.insert(len(self), item)

    # all add item should be here
    def insert(self, i, item):
        if self._before_add:
            self._before_add(item=item, obj=self)
        self.data.insert(i, item)

    def pop(self, i=-1):
        x = self[i]
        del self[i]
        return x

    def remove(self, item):
        i = self.index(item)
        del self[i]

    def clear(self):
        for i in range(len(self)):
            self.pop()

    def extend(self, other):
        for item in other:
            self.append(item)


