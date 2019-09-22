# -*- coding: utf-8 -*-

import coloredlogs
import logging
import json
import datetime
import jwt
import decimal
import traceback
import inspect

from .constants import Constants
from celery import Celery

constants = Constants()

class Util:

    def setup_logging(self):
        coloredlogs.install(level='INFO',
                            fmt='%(asctime)s %(name)-8s[%(process)d] %(levelname)8s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

    def list_to_json(self, l):
        return json.dumps(l, default=lambda o: o.__dict__)

    def make_json(self, cod_return, message, data):
        if isinstance(data, list) or isinstance(data, dict):
            json_data = {
                'cod_return' : cod_return,
                'message' : message, 
                'data' : data
            }
        else:
            json_data = {
                'cod_return' : cod_return,
                'message' : message, 
                'data' : json.loads(data)
            }

        return json.dumps(json_data)

    