""" File for send, edit and remove messages functions """

# Imports
from src.error import AccessError, InputError
from src.data import users, channels, dms
from datetime import datetime, timezone
from src.message_senddm_v2 import message_senddm_v2

# Send Message
def message_send_v1(auth_user_id, channel_id, message):
    ''' Function that sends message to a channel'''

    # Check that length of message is less than 1000 characters

    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')
    

    # Check that user is authorised to view channel 
    if is_user_authorised(auth_user_id, channel_id) == False:
        raise AccessError(description='User is not authorised to this channel')

    
    # Message Details

    total_messages = 0
    for channel in channels:
        total_messages = total_messages + len(channel['messages'])

    m_message_id = total_messages + 1
    m_u_id = auth_user_id
    m_message_string = message
    m_time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())


    # Find appropriate channel
    for channel in channels:
        if channel['id'] == channel_id['channel_id']:
            break

    channel['messages'].append(
        {
            'message_id' : m_message_id,
            'u_id': m_u_id,
            'message_string': m_message_string,
            'time': m_time,
        }
    )

    total_messages = total_messages + 1

    # Return message_id
    return {
        'message_id': m_message_id,
    }

# Edit message
def message_edit_v1(auth_user_id, message_id, message):
    ''' Function that edits message'''

    if valid_message_length(message) == False:
        raise InputError(description='Message is more than 1000 characters')

    if message_sent_by_user(auth_user_id, message_id) == False and is_user_owner(auth_user_id, message_id) == False:
        raise AccessError(description='Access Error')

    for channel in channels:
        for message_stored in channel['messages']:
            if message_id == {'message_id': message_stored['message_id']}:
                message_stored['message_string'] = message
    
    return {}

# Delete Message
def message_remove_v1(auth_user_id, message_id):
    ''' Function that removes message'''

    if message_exists(message_id) == False:
        raise InputError(description='Message no longer exists')

    if message_sent_by_user(auth_user_id, message_id) == False and is_user_owner(auth_user_id, message_id) == False:
        raise AccessError(description='Access Error')
    

    delete_message(message_id)
    return {}

# Share Message
def message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id):
    ''' Function that shares message to channel or DM'''

    if is_user_authorised(auth_user_id, channel_id) == False:
        raise AccessError(description='User has not joined the channel he is trying to share to')


    if len(message) == 0:
        message = ''
    

    if (dm_id == -1):
        shared_message_id = 0
        for channel in channels:
            for message in channel['messages']:
                if message['message_id'] == og_message_id['message_id']:
                    new_message = message['message_string']
                    shared_message_id = message_send_v1(auth_user_id, channel_id, new_message)


    if (channel_id == -1):
        for user in users:
            if user['u_id'] == auth_user_id:
                token = user['token']

        shared_message_id = 0
        for dm in dms:
            if dm_id == dm['dm_id']:
                for message in dm['messages']:
                    if (og_message_id == message['message_id']):
                        new_message = message['message_string']
                        shared_message_id = message_senddm_v2(token, dm_id, new_message)

                    

    return {'shared_message_id': shared_message_id}


    


# -----------------------
# Jack's Helper Functions
# -----------------------

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
            if message_id == {'message_id': message['message_id']}:
                if message['u_id'] == auth_user_id:
                    result = True
    return result

def get_user_from_token(token):   
    ''' Function that gets user ID from token''' 
    decoded_u_id = jwt.decode(token, data.SECRET, algorithms='HS256')    
    return decoded_u_id['u_id']

def message_exists(message_id):
    ''' Function that checks if a certain message exists'''
    exists = False 
    for channel in channels:
        for message in channel['messages']:
            if {'message_id': message['message_id']} == message_id:
                exists = True 
    return exists 

def delete_message(message_id):
    ''' Function that deletes a certain message'''
    for channel in channels:
        for message in channel['messages']:
            if message_id == {'message_id': message['message_id']}:
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
                if new_message == message['message_string']:
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
    
    #print(f"I am now in channel {channel['id']}")
    #print(len(channel['messages']))
    for message in channel['messages']:

        if {'message_id': message['message_id']} == message_id:
            #print(f"The only message I will work on is {message['message_id']}")
            shared = True
    return shared

