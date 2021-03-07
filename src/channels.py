from src.error import InputError
from src.data import users, channels

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }
#Creates a new channel with that name that is either a public or private channel
def channels_create_v1(auth_user_id, name, is_public):
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
        'id': channel_id,
    }

def check_channel_empty():
    if len(channels) == 0:
        return True
    return False

def last_channel_id():
    return channels[-1]['id']
