# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:42:15 2018

@author: user
"""

class Config(object):
    pass
class ProdConfig(Config):
    pass
class DevConfig(Config):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'