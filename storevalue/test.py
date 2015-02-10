#coding:utf-8
__author__ = 'qitian'

from os import sys, path
from sqlalchemy import create_engine
from apps.crm.member.storevalue import set_store_value
# from dboption import hello

# hello()

d = {'hell':'24', '234':'32'}
# print d.pop('helsl')

def test(key):
    try:
        print d.pop(key)
    except KeyError, e:
        print e
        raise Exception, e


print d.get('hsell', '234')
print
