import sys
import os

TOP_DIR = os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir, #上一级
    os.pardir
))

MARGS_DIR = os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    'margs'
))

USERINFO = os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    'userinfo'
))

DB_DIR = os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir, #上一级
    os.pardir,
    'db'
))


# print(aa)
# print(TOP_DIR)
# print(MARGS_DIR)