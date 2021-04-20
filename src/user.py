from src.error import InputError
from src.data import users, channels, dms
import re
from src.channel import token_to_id,  test_if_user_in_ch
import urllib
import urllib.request
import imghdr
from PIL import Image
import src.config
from src.dm import check_user_in_dm

def user_profile_v1(token, u_id):

    #auth_user_id = token_to_id(token)
    #auth user id - person logged in 
    # u_id - person whose profile you want to see
    exists = False
    for user in users:
        if user['u_id'] == u_id:
            exists = True

    if exists == False:
        raise InputError(description='User with u_id is not a valid user')

    for user in users:
        if user['u_id'] == u_id:
            new_u_id = user['u_id']
            new_email = user['email']
            new_name_first = user['name_first']
            new_name_last = user['name_last']
            new_handle = user['handle']
            
    
    return {
        'user': {
            'u_id': new_u_id,
            'email': new_email,
            'name_first': new_name_first,
            'name_last': new_name_last,
            'handle_str': new_handle,
        },
    }

def user_profile_setname_v1(token, name_first, name_last):

    auth_user_id = token_to_id(token)

    if len(name_first) <= 1:
        raise InputError(description='first name too short')
    if len(name_first) >= 50:
        raise InputError(description='first name too long')
    if len(name_last) <= 1:
        raise InputError(description='last name too short')
    if len(name_last) >= 50:
        raise InputError(description='last name too long')

        
    for user in users:
        if user['u_id'] == auth_user_id:
            user['name_first'] = name_first
            user['name_last'] = name_last

    return {
    }

def user_profile_setemail_v1(token, email):

    auth_user_id = token_to_id(token)

    if email_is_valid(email) == False:
        raise InputError(description='Email address is not valid')

    if is_email_used(email) == True:
        raise InputError(description='Email address is already being used by another user')

    for user in users:
        if user['u_id'] == auth_user_id:
            user['email'] = email
    return { }

def user_profile_sethandle_v1(token, handle_str):

    auth_user_id = token_to_id(token)
    if handle_str == None:
        raise InputError(description='hanlde string is empty')
    if len(handle_str) <= 3:
        raise InputError(description='new handle is too short')
    
    if len(handle_str) >= 20:
        raise InputError(description='new handle is too long')

    for user in users:
        if user['handle'] == handle_str:
            raise InputError(description='handle is in use')

    for user in users: 
        if user['u_id'] == auth_user_id:
            user['handle'] = handle_str 

    return {
    }

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    for user in users:
        if user['token'] == token:
            u_id = user['u_id']
            crop_img(img_url, x_start, y_start, x_end, y_end, u_id)
            user['profile_img_url'] = src.config.url + f"/static/avatar_{u_id}.jpg"
    
    return {}

#helpers 
def user_stats_v1(token):
    auth_user_id = token_to_id(token)
    num_msgs_sent = 0

    # find the number of channels that the user is a part of
    num_channels_joined = 0    
    for channel in channels:
        if (test_if_user_in_ch(auth_user_id, channel['id'])):
            num_channels_joined += 1
        num_msgs_sent += user_msgs_in_channel(auth_user_id, channel)        

    # find the number of dms that the user is a part of
    num_dms_joined = 0
    for dm in dms:
        if (check_user_in_dm(auth_user_id, dm['dm_id'])):
            num_dms_joined += 1
        num_msgs_sent += user_msgs_in_dm(auth_user_id, dm)    

    # involvement rate as defined by spec
    user_activity = num_channels_joined + num_dms_joined + num_msgs_sent
    possible_activity = num_dreams_channels() + num_dreams_dms() + num_dreams_msgs()
    involvement_rate = user_activity / possible_activity
    
    return {
        'user_stats' : {
            'channels_joined': users[auth_user_id]['timestamp_ch'],
            'dms_joined': users[auth_user_id]['timestamp_dm'],
            'messages_sent': users[auth_user_id]['timestamp_msg'],
            'involvement_rate': involvement_rate,
        }
    }

# jeff's stats helpers
def user_msgs_in_channel(auth_user_id, channel_dict):
    result = 0
    for msg in channel_dict['messages']:
        if msg['u_id'] == auth_user_id:
            result += 1
    return result

def user_msgs_in_dm(auth_user_id, dm_dict):
    result = 0
    for msg in dm_dict['messages']:
        if msg['u_id'] == auth_user_id:
            result += 1
    return result

def num_dreams_msgs():
    total = 0
    for channel in channels:
        total += len(channel['messages'])
    for dm in dms:
        total += len(dm['messages'])
    return total

def num_dreams_channels():
    return len(channels)

def num_dreams_dms():
    return len(dms)

#helpers 
def is_email_used(email):
    used = False
    for user in users:
        if user['email'] == email:
            used = True
    return used

def email_is_valid(email):
    '''checking for a valid email using regex'''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return bool(re.search(regex, email))

def crop_img(img_url, x_start, y_start, x_end, y_end, token):
    u_id = token_to_id(token)
    path = f"./static/avatar_{u_id}.jpg"
    urllib.request.urlretrieve(img_url, path)
    if imghdr.what(path) != 'jpeg':
        raise InputError(description='Image uploaded is not a JPG')
    img = Image.open(path)
    width,height = img.size
    if int(x_start) < 0 or int(x_end) > width or int(y_start) < 0 or int(y_end) >height:
        raise InputError(description='crop dimensions are not within the dimensions of the image.')
    cropped_img = img.crop((int(x_start), int(y_start), int(x_end), int(y_end)))
    cropped_img.save(path)
