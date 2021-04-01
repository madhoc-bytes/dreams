""" message.py file"""

from src.error import AccessError, InputError
from src.channels import channels_list_v1
from src.data import data
from datetime import datetime, timezone

def valid_message_length(message):
    if len(message) > 1000:
        return False
    else:
        return True

def channel_exists(channel_id):
    exists = False
    for channel in channels:
        if channel['id'] == channel_id:
            exists = True
    return exists

def user_exists(auth_user_id):
    exists = False
    for user in users:
        if user['u_id'] == auth_user_id:
            exists = True
    return exists
    
def user_authorised(auth_user_id, channel_id):
    authorised = False 
    channels_list = []
    channels_list = channels_list_v1(auth_user_id)
    for channel in channels_list:
        if channel['all_members']['u_id'] == channel_id:
            authorised = True
    return authorised

def user_authorised(auth_user_id, channel_id):
    authorised = False 
    for user in users:
        if user['u_id'] == auth_user_id:
            if user['token']:
                token = user['token']
                u_id_token = get_user_from_token(token)
                if auth_user_id == u_id_token:
                    authorised = True
                break
            else:
                break 
    return authorised 

def get_user_from_token(token):    
    decoded_u_id = jwt.decode(token, data.SECRET, algorithms='HS256')    
    return decoded_u_id['u_id']

def total_messages():
    length = 0
    for channel in channels:
        length = len(channel['messages'])
    return length 

def message_exists(message_id):
    exists = False 
    for channel in channels:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                exists = True 
    return exists 

def delete_message(message_id):
    for channel in channels:
        for message in channel['messages']:
            if message_id == message['message_id']:
                remove(message)
    return None

def message_send_v1(auth_user_id, channel_id, message):

    # Check that length of message is less than 1000 characters
    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')
    
    # Check that the channel for the given channel_id exists
    if channel_exists() == False:
        raise InputError(description='Channel does not exist')

    # Check that user for given auth_user_id exists
    if user_exists(auth_user_id) == False:
        raise InputError(description='User does not exist')

    # Check that user is authorised to view channel 
    if user_authorised() == False:
        raise AccessError(description='User is not authorised to this channel')

    # Message Details
    m_message_id = total_messages() + 1
    m_u_id = auth_user_id
    m_message_string = message
    time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())


    # Find appropriate channel
    for channel in channels:
        if channel['id'] == channel_id:
            break

    channel['messages'].append(
        {
            'message_id' : m_message_id,
            'u_id': m_u_id,
            'message': m_message,
            'time': m_time,
        }
    )

    total_messages = total_messages + 1

    # Return message_id
    return {
        'message_id': m_message_id,
    }

def message_edit_v1(auth_user_id, message_id, message):

    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')

    for message in channels['messages']:
        if message_id == message['message_id']:
            message['message_string'] = message
        
    return {}

def message_remove_v1(auth_user_id, message_id):

    if message_exists(message_id) == False:
        raise InputError(description='Message no longer exists')
    
    # CHECK FOR AccessError

    delete_message(message_id)
    return {}




