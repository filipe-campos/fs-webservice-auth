#!flask/bin/python
# -*- coding: utf-8 -*-
from route import *
from configuration import Configuration
from util import Constants, Util

from flask_cors import CORS
from flask import Flask, request, Response
from flask_mysqldb import MySQL

constants = Constants()
configuration = Configuration()
util = Util()
mySQL = MySQL()

#Routes
authRoute = AuthRoute()

#Flask Configuration
app = Flask(__name__)
CORS(app)

#MySQL Configuration
app.config['MYSQL_HOST'] = configuration.MYSQL_HOST
app.config['MYSQL_PORT'] = configuration.MYSQL_PORT
app.config['MYSQL_USER'] = configuration.MYSQL_USER
app.config['MYSQL_PASSWORD'] = configuration.MYSQL_PASS
app.config['MYSQL_DB'] = configuration.MYSQL_DB

mySQL.init_app(app)

## -- AUTH -- ##
@app.route('/dashboard/api/v1.0/auth/login', methods=['POST'])
def login():
    return Response(authRoute.login(request), mimetype='application/json')

@app.route('/dashboard/api/v1.0/auth/password/check', methods=['POST'])
def check_password():
    return Response(authRoute.check_password(request), mimetype='application/json')

@app.route('/dashboard/api/v1.0/auth/token/check', methods=['POST'])
def check_token():
    return Response(authRoute.check_token(request), mimetype='application/json')

@app.route('/dashboard/api/v1.0/auth/logout', methods=['POST'])
def logout():
    return Response(authRoute.logout(request), mimetype='application/json')

if __name__ == '__main__':
    #app.run(host='dashboard.fiscoserv.com.br', port=5001, ssl_context=('fullchain.pem', 'privkey.pem'), debug=False)
    app.run(host='127.0.0.1', port=5001)
    #app.run(host='10.0.0.187', port=5001)
