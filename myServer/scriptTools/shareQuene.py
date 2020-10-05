from multiprocessing import Manager,Process
import time

class SingletonQuene(object):
    def __init__(self):
        self.m = Manager()
        self.rl = self.m.RLock()
        self.q = self.m.Queue(maxsize=100)


    def dealJob(self):
        job = self.q.get()
        print(job)

#  解释 python 包文件 是 天然 单例模式，这样整个程序中， 只会初始化 一个 内置消息队列

shareQ = SingletonQuene()