from src.data import users, channels
from src.channel import test_user_is_invalid
from src.error import InputError, AccessError

''' Resets the internal data of the application to it's initial state '''
def clear_v1():
    users.clear()
    channels.clear()

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def adminuserpermissionchangev1(token, u_id, permission_id):
    check_if_token_valid(token) 
    #$check valid user
    test_user_is_invalid(u_id)
    token_uid = importuIDfromtoken(token)
    #If permission_id invalid
    if permission_id < 1 or permission_id > 2:
        raise InputError('perjmission_id invalid')

    #If token is not owner
    not_owner = True
    for user in users:
        if user['u_id'] == token_uid:
            if user['permission'] == 1:
                not_owner = False
                break 

    if not_owner:
        raise AccessError("Authorised user is not owner")
    data_change_permission(u_id, permission_id)
    
#helper
def data_change_permission(u_id, permission_id): 
    for user in data['users']: 
        if user['u_id'] == u_id: 
            user['permission_id'] = permission_id 
            return
''' create len of channels to check if clear'''
def data_channels():
    return len(channels)
''' create len of users to check if clear'''
def data_user():
    return len(users)
def importuIDfromtoken(token):
    return
def check_if_token_valid(token):
    if not if_token_exit(token) or token == None:
        raise AccessError('Invalid Token')
    return
def if_token_exit(token):
    for user in users:
        if token == user[token]:
            return user
    return False
