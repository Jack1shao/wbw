#encoding=utf-8
#装饰模式（Decorator）
__author__ = 'kevinlu1010@qq.com'

from abc import ABCMeta, abstractmethod


class Person():
    def __init__(self, name):
        self.name = name
        print("1、"+name)
    def decorator(self, component):
        self.component = component
        print("55555")

    def show(self):
        print ('%s开始穿衣' % self.name)

        self.component.show()



class Finery():
    def __init__(self):
        self.component = None
        print("2、")

    def decorator(self, component):
        self.component = component
        print("44444")

    __metaclass__ = ABCMeta

    @abstractmethod
    def show(self):
        if self.component:
             self.component.show()
            


class TShirt(Finery):
    def show(self):
        Finery.show(self)
        print('穿TShirst')


class Trouser(Finery):
    def show(self):
        Finery.show(self)
        print ('穿裤子')


class Shoe(Finery):
    def show(self):
        Finery.show(self)
        print ('穿鞋子')


class Tie(Finery):
    def show(self):
        Finery.show(self)
        print ('穿领带')


if __name__ == '__main__':
    person = Person('kevin')
    tshirt = TShirt()
    trouser = Trouser()
    shoe = Shoe()
    tie = Tie()
    print("333-3")

    trouser.decorator(tshirt)
    shoe.decorator(trouser)
    tie.decorator(shoe)
    person.decorator(tie)
    #person.decorator(tshirt)
    person.show()

   # print(person.name)