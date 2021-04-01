# pylint: disable=W0613
"""channels.py file"""

# Imports
from src.channel import test_if_user_in_ch
from src.data import channels
from src.error import InputError

def channels_list_v2(token):
    """Function that lists all channels for which a certain user has access"""

    # Get user ID from token
    auth_user_id = get_user_from_token(token)

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



def channels_create_v1(auth_user_id, name, is_public):
    """Function that creates channel"""

    ## check if the name is more than 20 raise an Inputerror
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long!")
    if check_channel_empty():
        # if the channel is empty
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

    return {
        'channel_id': channel_id,
    }

def check_channel_empty():
    """Function that checks if channel is empty"""
    if len(channels) == 0:
        return True
    return False

def last_channel_id():
    """Function that checks last channel ID"""
    return channels[-1]['id']




