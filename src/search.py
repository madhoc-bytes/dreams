from src.data import users, channels, dms
from src.error import InputError, AccessError
from src.channel import test_if_user_in_ch
from src.channel import token_to_id
from src.dm import check_user_in_dm

def search_v2(token, query_str):
    u_id = token_to_id(token) 
    # string is too long
    if len(query_str) > 1000:
        raise InputError()

    participated_channels = channels_related_to_user(u_id)
    participated_dms = dms_related_to_user(u_id)

    found_messages = []

    for channel in participated_channels:
        for msg in channel['messages']:
            if query_str in msg['message_string']:
                found_messages.append(msg['message_string'])

    for dm in participated_dms:
        for msg in dm['messages']:
            if query_str in msg['message']:
                found_messages.append(msg['message'])
    
    return {'messages' : found_messages}

# return a list of channels that user is a part of
def channels_related_to_user(u_id):
    participated_channels = []
    for channel in channels:
        if (test_if_user_in_ch(u_id, channel['id'])):
            participated_channels.append(channel)
    return participated_channels

# return a list of dms that user is a part of
def dms_related_to_user(u_id):
    participated_dms = []
    for dm in dms:
        if (check_user_in_dm(u_id, dm['dm_id'])):
            participated_dms.append(dm)
    return participated_dms
