# coding=utf-8

from abc import abstractmethod


class Base(object):
    @abstractmethod
    def to_element(self):
        pass
