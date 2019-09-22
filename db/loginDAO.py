# -*- coding: utf-8 -*-
import mysql.connector
import json
import inspect
import traceback

from util import Util, Log, CodeReturn
from controller import Controller
from configuration import Configuration
from flask import Flask
from flask_mysqldb import MySQL

log = Log('LoginDAO')
configuration = Configuration()
controller = Controller()
codeReturn = CodeReturn()
util = Util()
mySQL = MySQL()

app = Flask(__name__)

class LoginDAO:
    def __init__(self):
        mySQL.init_app(app)
    
    def login(self, user, password):
        try:
            user_data = {
                "token" : None,
                "name_user" : None,
                "email_user" : None,
                "type_user" : None,
                "image" : None,
                "companies" : []
            }

            cursorMySQL = mySQL.connection.cursor()

            queryMySQL = ("SELECT id, name, email, type_user, image, plan_id "
                          "FROM user "
                          "WHERE user = '"+str(user)+"' AND pass = '"+str(password)+"';")

            cursorMySQL.execute(queryMySQL)
            rowMySQL = cursorMySQL.fetchone()

            if(rowMySQL == None):
                return codeReturn.WRONG_LOGIN_CODE, codeReturn.WRONG_LOGIN_MSG, []
            else:
                user_data["token"] = str(controller.encode_auth_token(rowMySQL[0]).decode("utf-8"))
                user_data["name_user"] = rowMySQL[1]
                user_data["email_user"] = rowMySQL[2]
                user_data["type_user"] = str(controller.encode_token(rowMySQL[3]).decode("utf-8"))
                user_data["image"] = rowMySQL[4]
                user_data["plan_token"] = str(controller.encode_token(rowMySQL[5]).decode("utf-8"))

            queryMySQL = ("SELECT user_id, name_user, email_user, type_user, image, plan_id, "
                          "company_id, name_company, cnpj, last_export "
                          "FROM vw_user_has_company "
                          "WHERE user = '"+str(user)+"' AND pass = '"+str(password)+"';")

            cursorMySQL.execute(queryMySQL)

            for rowMySQL in cursorMySQL:
                user_data["companies"].append({
                    "company_token": str(controller.encode_token(rowMySQL[6]).decode("utf-8")),
                    "name_company": rowMySQL[7],
                    "cnpj": rowMySQL[8],
                    "last_export": rowMySQL[9].strftime("%d/%m/%Y")
                })

            cursorMySQL.close()

        except:
            log.error(inspect.getframeinfo(inspect.currentframe()).function, 
                      str(traceback.format_exc()), 
                      0)

            return codeReturn.UNKNOW_ERROR_CODE, codeReturn.UNKNOW_ERROR_MSG, []
        
        return codeReturn.SUCCESS_CODE, codeReturn.SUCCESS_MSG, json.dumps(user_data)

    def check_password(self, password, user_id):
        try:

            cursorMySQL = mySQL.connection.cursor()

            queryMySQL = ("SELECT id "
                          "FROM user "
                          "WHERE id = '"+str(user_id)+"' AND pass = '"+str(password)+"';")

            cursorMySQL.execute(queryMySQL)
            rowMySQL = cursorMySQL.fetchone()

            if(rowMySQL == None):
                return codeReturn.WRONG_LOGIN_CODE, codeReturn.WRONG_LOGIN_MSG, []
            else:
                return codeReturn.SUCCESS_CODE, codeReturn.SUCCESS_MSG, []
                
            cursorMySQL.close()
        except:
            log.error(inspect.getframeinfo(inspect.currentframe()).function, 
                      str(traceback.format_exc()), 
                      0)

            return codeReturn.UNKNOW_ERROR_CODE, codeReturn.UNKNOW_ERROR_MSG, []
