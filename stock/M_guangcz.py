# 主题行为类
#观察者模式
class NewsPublisher:
    def __init__(self):
        self.__subscribers = [] # 存放这个类的对象的观察者们
        self.__latestNews = None

    # 观察者通过这个方法注册进来，放在客户端的列表里
    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    # 删除观察者
    def detach(self):
        return self.__subscribers.pop()

    # 返回已经注册的所有观察者
    def subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    # 遍历所有观察者，通过观察者的update方法打印出观察者获取的最新消息
    def notify_subscribers(self):
        for sub in self.__subscribers:
            sub.update()

    # 添加新消息
    def add_news(self, news):
        self.__latestNews = news

    # 返回最新消息
    def get_news(self):
        return self.__latestNews


# 观察者接口，抽象方法
from abc import ABCMeta, abstractmethod
class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass


# 观察者email
class EmailSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


# 观察者sms
class SMSSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


# 用来演示Observers和Subject的松耦合关系
class AnyOtherSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


if __name__ == '__main__':
    # 创建一个客户端对象
    news_publisher = NewsPublisher()

    # 创建3个观察者
    for subscribers in [SMSSubscriber, EmailSubscriber, AnyOtherSubscriber]:
        subscribers(news_publisher)

    # 打印出所有观察者列表
    print('\nsubscribers:', news_publisher.subscribers())

    # 添加一个消息
    news_publisher.add_news('hello')

    # 提醒所有观察者新消息，
    news_publisher.notify_subscribers()

    print(type(news_publisher.detach()).__name__)
    print(news_publisher.subscribers())

    news_publisher.add_news('第二个消息')
    news_publisher.notify_subscribers()
