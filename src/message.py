""" File for send, edit and remove messages functions """

# Imports
from src.error import AccessError, InputError
import jwt
from src.data import users, channels, dms, dreams
from src.channel import token_to_id, test_user_is_invalid, test_channel_is_invalid, test_if_user_in_ch 
from datetime import datetime, timezone
from src.dm import test_dm_is_invalid, check_user_in_dm
from src.message_senddm_v2 import message_senddm_v2
from threading import Timer
from time import mktime

# Send Message
def message_send_v2(token, channel_id, message):
    ''' Function that sends message to a channel'''

    auth_user_id = token_to_id(token)

    # Check that length of message is less than 1000 characters
    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')
    
    
    # Check that user is authorised to view channel 
    if is_user_authorised(auth_user_id, channel_id) == False:
        raise AccessError(description='User is not authorised to this channel')

    
    # Message Details
    m_message_id = get_current_message_id()
    m_message_id = m_message_id + 1
    m_u_id = auth_user_id
    m_message = message
    m_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())

    # Find appropriate channel
    for channel in channels:
        if {'channel_id': channel['id']} == channel_id or channel['id'] == channel_id:
            break


    channel['messages'].append(
        {
            'message_id' : m_message_id,
            'u_id': m_u_id,
            'message': m_message,
            'time_created': m_time,
            'reacts': [],
            'is_pinned': False,
        }
    )
    # user analytics
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    users[auth_user_id]['num_messages_sent'] += 1
    users[auth_user_id]['timestamp_msg'].append({
        'num_messages_sent': users[auth_user_id]['num_messages_sent'],
        'time_stamp': time_now,
    })

    # dreams analytics
    dreams['msgs'] += 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_msg'].append({
        'num_messages_exist': dreams['msgs'], 
        'time_stamp': time_now,
    })

    # Return message_id
    return {
        'message_id': m_message_id,
    }

# Edit message
def message_edit_v1(token, message_id, message):
    ''' Function that edits message'''
    auth_user_id = token_to_id(token)

    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')

    if message_sent_by_user(auth_user_id, message_id) == False and is_user_owner(auth_user_id, message_id) == False:
        raise AccessError(description='Access Error')

    for channel in channels:
        for message_stored in channel['messages']:
            if message_id == {'message_id': message_stored['message_id']}:
                message_stored['message'] = message
    
    return {}

# Delete Message
def message_remove_v1(token, message_id):
    ''' Function that removes message'''
    auth_user_id = token_to_id(token)


    if message_exists(message_id) == False:
        raise InputError(description='Message no longer exists')


    if message_sent_by_user(auth_user_id, message_id) == False and is_user_owner(auth_user_id, message_id) == False:
        raise AccessError(description='Access Error')

    # user analytics
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    users[auth_user_id]['num_messages_sent'] -= 1
    users[auth_user_id]['timestamp_msg'].append({
        'num_messages_sent': users[auth_user_id]['num_messages_sent'],
        'time_stamp': time_now,
    })
    delete_message(message_id)

    # dreams analytics
    dreams['msgs'] -= 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_msg'].append({
        'num_messages_exist': dreams['msgs'], 
        'time_stamp': time_now,
    })

    return {}

# Share Message
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    ''' Function that shares message to channel or DM'''
    auth_user_id = token_to_id(token)

    if len(message) == 0:
        message = ''
    

    if (dm_id == -1):
        if is_user_authorised(auth_user_id, channel_id) == False:
            raise AccessError(description='User has not joined the channel he is trying to share to')
        shared_message_id = 0
        for channel in channels:
            for message in channel['messages']:
                if og_message_id == {'message_id': message['message_id']}:
                    new_message = message['message']
                    shared_message_id = message_send_v2(token, channel_id, new_message)


    if (channel_id == -1):
        if is_user_in_dm(auth_user_id, dm_id) == False:
            raise AccessError(description='User has not joined the DM he is trying to share to')
        for user in users:
            if user['u_id'] == auth_user_id:
                token = user['token']

        shared_message_id = 0
        for dm in dms:
            for message in dm['messages']:
                if og_message_id == {'message_id': message['message_id']}:
                    new_message = message['message']
                    shared_message_id = message_senddm_v2(token, dm_id, new_message)
    # user analytics
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    users[auth_user_id]['num_messages_sent'] += 1
    users[auth_user_id]['timestamp_msg'].append({
        'num_messages_sent': users[auth_user_id]['num_messages_sent'],
        'time_stamp': time_now,
    })
    
    # dreams analytics
    dreams['msgs'] += 1
    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    dreams['timestamp_msg'].append({
        'num_messages_exist': dreams['msgs'], 
        'time_stamp': time_now,
    })

    return {'shared_message_id': shared_message_id}


# Pin Message
def message_pin_v1(token, message_id):
    auth_user_id = token_to_id(token)

    if message_exists(message_id) == False:
        raise InputError(description='Message does not exist')

    if message_is_pinned(message_id) == True:
        raise InputError(description='Message is already pinned')


    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                channel_id = channel['id']
                if is_user_authorised(auth_user_id, {'channel_id': channel_id}) == False and is_user_owner(auth_user_id, message_id) == False:
                    raise AccessError(description='User is not authorised or user is not owner of the channel')
                message['is_pinned'] = True


    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                dm_id = dm['dm_id']
                if is_user_in_dm(auth_user_id, dm_id) == False:
                    raise AccessError(description='User is not authorised to the DM')
                message['is_pinned'] = True

# Unpin Message
def message_unpin_v1(token, message_id):
    auth_user_id = token_to_id(token)

    if message_exists(message_id) == False:
        raise InputError(description='Message does not exist')

    if message_is_unpinned(message_id) == True:
        raise InputError(description='Message is already unpinned')

        
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                channel_id = channel['id']
                if is_user_authorised(auth_user_id, {'channel_id': channel_id}) == False and is_user_owner(auth_user_id, message_id) == False:
                    raise AccessError(description='User is not authorised or user is not owner of the channel')
                message['is_pinned'] = False

    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                dm_id = dm['dm_id']
                if is_user_in_dm(auth_user_id, dm_id) == False:
                    raise AccessError(description='User is not authorised to the DM')
                message['is_pinned'] = False


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''Send a message to a channel at a specified time in the future'''
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    if test_channel_is_invalid(channel_id):
        raise InputError()
    if len(message) > 1000:
        raise InputError()
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()

    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    if time_now > time_sent:
        raise InputError()
    
    seconds_after = time_sent - time_now
    #start message_send after '_a sec 
    Timer(seconds_after, message_send_v2, [token, channel_id, message]).start()

    message_id = get_current_message_id()
    message_id = message_id + 1
    
    return {"message_id": message_id}

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    #if dm_id not valid dm -> inputer
    if test_dm_is_invalid(dm_id):
        raise InputError()
    if len(message) > 1000:
        raise InputError()
    # invalid user
    if not check_user_in_dm(auth_user_id, dm_id):
        raise AccessError()


    time_now = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    if time_now > time_sent:
        raise InputError()
    
    seconds_after = time_sent - time_now
    #start message_senddm after seconds_after has past
    Timer(seconds_after, message_senddm_v2, [token, dm_id, message]).start()

    message_id = get_current_message_id()
    message_id = message_id + 1
    return {"message_id": message_id}

def message_react_v1(token, message_id, react_id):
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    ## ADD MORE TO HERE IN FUTURE IF NEED MORE
    valid_reacts = [1]
    if react_id not in valid_reacts:
        raise InputError()

    msg = get_message_from_mid(message_id)

    if msg == {}:
        raise InputError()
    
    if len(msg['reacts']) != 0:
        for react in msg['reacts']:
            key, value = 'react_id', react_id
            if key in react and value == react[key]:
                if auth_user_id in react['u_ids']:
                    raise InputError()
                else:
                    react['u_ids'].append(auth_user_id)
                    react['is_this_user_reacted'] = True
    else:
        newreact = {
            'react_id': react_id,
            'u_ids': [auth_user_id],
            'is_this_user_reacted': True
        }
        msg['reacts'].append(newreact)

    return {}

def message_unreact_v1(token, message_id, react_id):
    auth_user_id = token_to_id(token)
    if test_user_is_invalid(auth_user_id):
        raise InputError()
    ## ADD MORE TO HERE IN FUTURE IF NEED MORE
    valid_reacts = [1]
    if react_id not in valid_reacts:
        raise InputError()

    msg = get_message_from_mid(message_id)

    if msg == {}:
        raise InputError()

    if len(msg['reacts']) == 0:
        raise InputError()
    
    for react in msg['reacts']:
        key, value = 'react_id', react_id
        if key in react and value == react[key]:
            if len(react['u_ids']) != 1:
                if auth_user_id in react['u_ids']:
                    react['u_ids'].remove(auth_user_id)
                else:
                    raise InputError
            else:
                msg['reacts'].remove(react)
    return {}


# helper functions

def valid_message_length(message):
    ''' Function that checks if the length of a message is valid'''
    if len(message) > 1000:
        return False
    else:
        return True

def is_user_authorised(auth_user_id, channel_id):
    ''' Function that checks if user is member of a channel'''

    authorised = False 
    for channel in channels:
        if channel_id == {'channel_id': channel['id']}:
            break
   
    for member in channel['all_members']:
        if member['u_id'] == auth_user_id:
            authorised = True
            break
    
    return authorised 

def message_sent_by_user(auth_user_id, message_id):
    ''' Function that checks if a message is sent by a certain user'''
    result = False
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['u_id'] == auth_user_id:
                    result = True

    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['u_id'] == auth_user_id:
                    result = True
    return result

def message_exists(message_id):
    ''' Function that checks if a certain message exists'''
    exists = False 
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                exists = True 

    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                exists = True
    return exists 

def delete_message(message_id):
    ''' Function that deletes a certain message'''
    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                dm['messages'].remove(message)

    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                channel['messages'].remove(message)
    return None

def is_user_owner(auth_user_id, message_id):
    ''' Function that checks if a user is the owner of a channel'''
    result = False 
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']}:
                break
            
        for member in channel['owner_members']:
            if auth_user_id == member['u_id']:
                result = True

    return result

def is_message_edited(message_id, new_message):
    ''' Function that checks if a message was edited successfully'''
    message_test = False
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']}:
                if new_message == message['message']:
                    message_test = True 
    return message_test

def is_message_deleted(message_id):
    ''' Function that checks if a message was deleted successfully'''
    result = True 
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']}:
                result = False
    return result 

def is_message_shared(message_id, channel_id):
    ''' Function that checks if a message was sent/shared successfully'''
    shared = False
    for channel in channels:
        if channel['id'] == channel_id['channel_id']:
            break
    
    for message in channel['messages']:
        if {'message_id': message['message_id']} == message_id:
            shared = True
    return shared

def is_message_in_dm(dm_id, message_id):
    ''' Function that checks if a message is in a DM '''
    result = False
    for dm in dms:
        if dm_id == dm['dm_id']:
            for message in dm['messages']:
                if message_id == message['message_id']:
                    result = True
    return result

def is_user_in_dm(auth_user_id, dm_id):
    ''' Function that checks if a user is in a DM '''
    result = False
    for dm in dms:
        if dm['dm_id'] == dm_id:
            break
    for user in dm['all_members']:
        if user['u_id'] == auth_user_id:
            result = True
    return result


def message_is_pinned(message_id):
    ''' Function that checks if a certain message is pinned'''
    pinned = False 
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['is_pinned'] == True:
                    pinned = True

    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['is_pinned'] == True:
                    pinned = True
    return pinned 

def message_is_unpinned(message_id):
    ''' Function that checks if a certain message is unpinned'''
    unpinned = False 
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['is_pinned'] == False:
                    unpinned = True

    for dm in dms:
        for message in dm['messages']:
            if message_id == {'message_id': message['message_id']} or message_id == message['message_id']:
                if message['is_pinned'] == False:
                    unpinned = True
    return unpinned 

def get_current_message_id():
    num_messages = -1
    for channel in channels:
        num_messages = num_messages + len(channel['messages'])

    for dm in dms:
        num_messages = num_messages + len(dm['messages'])

    return num_messages

def get_message_from_mid(message_id):
    for dm_id in range(len(dms)):
        for msg in dms[dm_id]['messages']:
            key, value = 'message_id', message_id
            if key in msg and value == msg[key]:
                return msg


    for ch_id in range(len(channels)):
        for msg in channels[ch_id]['messages']:
            key, value = 'message_id', message_id
            if key in msg and value == msg[key]:
                return msg
    
    return {}

