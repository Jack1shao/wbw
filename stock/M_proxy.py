#encoding=utf-8
#代理模式（Proxy）
__author__ = 'kevinlu1010@qq.com'
from abc import ABCMeta, abstractmethod


class FemaleA():
    def __init__(self, name):
        self.name = name


class Male():
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_flower(self):
        print(1)
        pass

    @abstractmethod
    def send_chocolate(self):
        pass

    @abstractmethod
    def send_book(self):
        pass


class MaleA(Male):
    def __init__(self, name, love_female):
        self.name = name
        self.love_female = FemaleA(love_female)

    def send_flower(self):
        print ('%s送花给%s' % (self.name, self.love_female.name))

    def send_chocolate(self):
        print ('%s送巧克力给%s' % (self.name, self.love_female.name))

    def send_book(self):
        print ('%s送书给%s' % (self.name, self.love_female.name))


class Proxy(Male):
    def __init__(self, name, proxyed_name, love_female):
        self.name = name
        self.proxyed = MaleA(proxyed_name, love_female)

    def send_flower(self):
        self.proxyed.send_flower()

    def send_chocolate(self):
        self.proxyed.send_chocolate()

    def send_book(self):
        self.proxyed.send_book()


if __name__ == '__main__':
    p = Proxy('男B', '男122A', '女A')
    p.send_book()
    p.send_chocolate()
    p.send_flower()