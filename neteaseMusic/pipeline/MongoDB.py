# coding=utf-8

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['cloudmusic']

def Insert_SongsInfo():
    pass