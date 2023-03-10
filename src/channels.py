from src.channel import test_if_user_in_ch
from src.channel import token_to_id
from src.data import channels, users, dreams
from src.error import InputError, AccessError
import jwt
from datetime import datetime, timezone

def channels_list_v2(token):
    """Function that lists all channels for which a certain user has access"""

    auth_user_id = token_to_id(token)
    # Create empty list to store channels details
    channels_details_list = []

    for channel in channels:
        # Check if the user has access to the channel to get details
        if test_if_user_in_ch(auth_user_id, channel['id']):
            channels_details_list.append({
                'name': channel['name'],
                'all_members': channel['all_members']
            })

    # Return the list
    return {
        'channels': channels_details_list
    }

def channels_listall_v2(token):
    """Function that lists all channels"""

    # Create empty list to store all channel details
    channels_details_list = []
    # Go through all channels and store details for each one of them
    for channel in channels:
        channels_details_list.append({
            'name': channel['name'],
            'all_members': channel['all_members']
        })
    # Return the list
    return {'channels': channels_details_list}

def channels_create_v2(token, name, is_public):
    """Function that creates channel"""
    #check valid token#
    check_token(token)
    ## check if the name is more than 20 raise an Inputerror
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long!")
    if check_channel_empty():
        # if the server is empty
        channel_id = 0
    else:
        #last channels id plus 1
        channel_id = last_channel_id() + 1
    new_channel = {
        'id': channel_id,
        'is_public': is_public,
        'name': name,
        'owner_members': [],
        'all_members': [],
        'messages': [],
    }
    channels.append(new_channel)
    
    # dreams analytics
    dreams['channels'] += 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_ch'].append({
        'num_channels_exist': dreams['channels'], 
        'time_stamp': time_now,
    })

    return {
        'channel_id': channel_id,
    }
#helper function#
def check_channel_empty():
    """Function that checks if channel is empty"""
    if len(channels) == 0:
        return True
    return False

def last_channel_id():
    """Function that checks last channel ID"""
    return channels[-1]['id']

def if_token_exit(token):
    for user in users:
        if token == user['token']:
            return user
    return False
def check_token(token):
    if not if_token_exit(token) or token == None:
        raise AccessError('Invalid Token Please change')
    return
