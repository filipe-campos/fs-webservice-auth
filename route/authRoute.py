# -*- coding: utf-8 -*-
import inspect
import traceback

from db import LoginDAO
from util import Util, Constants, Log, CodeReturn
from controller import Controller

log = Log('AuthRoute')
util = Util()
constants = Constants()
loginDAO = LoginDAO()
controller = Controller()
codeReturn = CodeReturn()

class AuthRoute:
    
    def login(self, request):
        if (request.is_json):
            try:
                content = request.get_json()

                #Get datas from JSON
                user = str(content['user'])
                password = str(content['pass'])
            except:
                return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

            code, msg, data = loginDAO.login(user, password)
            
            return util.make_json(code, msg, data)
        else:
            return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

    def check_password(self, request):
        if (request.is_json):
            try:
                content = request.get_json()
                header = request.headers

                #Get Token from Header
                token = str(header['token'])
                #Get datas from JSON
                data = json.loads(str(content['data']).replace("'",'"'))

                password = data['pass']
            except:
                return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

            #Authentication
            decode_auth_token = controller.decode_auth_token(token)

            if(decode_auth_token == codeReturn.EXPIRED_TOKEN_CODE):
                log.warning(inspect.getframeinfo(inspect.currentframe()).function, 
                            str(codeReturn.EXPIRED_TOKEN_MSG), 
                            0)

                return util.make_json(codeReturn.EXPIRED_TOKEN_CODE, codeReturn.EXPIRED_TOKEN_MSG, [])

            elif(decode_auth_token == codeReturn.INVALID_TOKEN_CODE):
                log.error(inspect.getframeinfo(inspect.currentframe()).function, 
                          str(codeReturn.INVALID_TOKEN_MSG), 
                          0)

                return util.make_json(codeReturn.INVALID_TOKEN_CODE, codeReturn.INVALID_TOKEN_MSG, [])
            else:
                code, msg, data = loginDAO.check_password(password, decode_auth_token)

                return util.make_json(code, msg, data)
        else:
            return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

    def check_token(self, request):
        if (request.is_json):
            try:
                header = request.headers

                #Get Token from Header
                token = str(header['token'])
            except:
                log.error(inspect.getframeinfo(inspect.currentframe()).function, 
                      str(traceback.format_exc()), 
                      0)
                return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

            #Authentication
            decode_auth_token = controller.decode_auth_token(token)

            if(decode_auth_token == codeReturn.EXPIRED_TOKEN_CODE):
                log.warning(inspect.getframeinfo(inspect.currentframe()).function, 
                            str(codeReturn.EXPIRED_TOKEN_MSG), 
                            0)

                return util.make_json(codeReturn.EXPIRED_TOKEN_CODE, codeReturn.EXPIRED_TOKEN_MSG, [])
            elif(decode_auth_token == codeReturn.INVALID_TOKEN_CODE):
                log.error(inspect.getframeinfo(inspect.currentframe()).function, 
                          str(codeReturn.INVALID_TOKEN_MSG), 
                          0)

                return util.make_json(codeReturn.INVALID_TOKEN_CODE, codeReturn.INVALID_TOKEN_MSG, [])
            else:
                return util.make_json(codeReturn.SUCCESS_CODE, codeReturn.SUCCESS_MSG, {
                    'id':decode_auth_token
                })
        else:
            return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])

    def logout(self, request):
        if request.is_json:
            return util.make_json(codeReturn.SUCCESS_CODE, codeReturn.SUCCESS_MSG, [])     
        else:
            return util.make_json(codeReturn.BAD_REQUEST_CODE, codeReturn.BAD_REQUEST_MSG, [])
