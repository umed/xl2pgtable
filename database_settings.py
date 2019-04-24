# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:09:51 2019

@author: PuchkovaKS
"""


class DatabaseSettings:
    user = "postgres"
    password = "pswd"
    database = "postgres"
    host = "172.17.0.1"
    schema = "public"

    def __iter__(self):
        yield "database", self.database
        yield "host", self.host
        yield "user", self.user
        yield "password", self.password
