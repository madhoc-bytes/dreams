# channels.py file

# Imports 
from src.channel import test_if_user_in_ch
from src.data import channels
from src.channel import channel_details_v1

# Function assume that channels_create_v1() 
# appends all_members and owner_members lists

def channels_list_v1(auth_user_id):    

    # Create emppty list to store channels details
    channels_details_list = []

    for channel in channels:
        # Check if the user has access to the channel to get details
        if (test_if_user_in_ch(auth_user_id, {'id': channel['id']})):
            channels_details_list.append({
                'name': channel['name'],
                'all_members': channel['all_members']
            })
    
    # Return the list
    return channels_details_list


# Function assumes that channels_create_v1() is fixed 
# because owner_members and all_members are empty

def channels_listall_v1(auth_user_id):

    # Create empty list to store all channel details
    channels_details_list = []
    # Go through all channels and store details for each one of them
    for channel in channels:
            channels_details_list.append({
                'name': channel['name'],
                'all_members': channel['all_members']
            })
    # Return the list
    return channels_details_list



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
