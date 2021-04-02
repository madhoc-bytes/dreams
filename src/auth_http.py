
from error import InputError, AccessError
from src import auth
from json import dumps
from flask import FLASK, request, requests
from src import server
from src.data import users

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():

    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return_value = auth_register_v1(email, password)
    return dumps(return_value)

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():

    email = request.form.get('email')
    password = request.form.get('password')
    return_value = auth_login_v1(email, password)
    return dumps(return_value)

@APP.route('/auth/logout/v2', methods=['POST'])
def auth_logout():

    token = request.form.get('token')
    return_value = auth_logout_v1(token)
    return dumps(return_value)