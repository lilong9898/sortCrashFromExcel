#! /usr/bin/python3.5
#coding=utf-8

# 这个类代表一个用户（即一个i号）
class User:

    def __init__(self, strUser):

        # 在某条去重后的错误中的出现次数
        self.count = 1;

        # 该用户的i号
        self.strUser = strUser;
    pass

    def toString(self):
        return self.strUser;

pass
