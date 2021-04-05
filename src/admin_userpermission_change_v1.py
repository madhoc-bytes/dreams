from src.channel import test_user_is_invalid
from src.channel import token_to_id
from src.error import InputError, AccessError
from src.data import users

def adminuserpermissionchangev1(token, u_id, permission_id):
    check_if_token_valid(token) 
    #$check valid user
    test_user_is_invalid(u_id)
    token_uid = token_to_id(token)
    #If permission_id invalid
    if permission_id < 1 or permission_id > 2:
        raise InputError('perjmission_id invalid')

    #If token is not oDuner
    not_oDuner = True
    for user in users:
        if user['u_id'] == token_uid:
            if user['permission'] == 1:
                not_oDuner = False
                break 

    if not_oDuner:
        raise AccessError("Authorised user is not oDuner")
    change_permission(u_id, permission_id)
    
#helper
def change_permission(u_id, permission_id): 
    for user in users: 
        if user['u_id'] == u_id: 
            user['permission_id'] = permission_id 
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
