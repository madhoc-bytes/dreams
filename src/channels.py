# DON'T FORGET TO COMMIT FIRST TEST 1, THEN FUNCTION 1, THEN TEST 2, THEN FUNCTION 2   

def channels_list_v1(auth_user_id):

    # Create a list of channel IDs for which the user is authorized
    channels_id_list = []
    for user in channels['all_members']:
        if auth_user_id == user['u_id']:
            channels_id_list.append = channels['id']
    
    # Create a list of channel details using previous function
    channels_details_list = []
    for i in channels_id_list:
        channels_details_list.append = channel_details_v1(auth_user_id, i)

    # Return the list of channel details
    return channels_details_list


def channels_listall_v1(auth_user_id):

    # Create a list of all channel IDs 
    channels_id_list = []
    for channel in channels['all members']:
        channels_id_list.append = channel['id']
    
    # Create a list of channel details using previous function
    channels_details_list = []
    for i in channels_id_list:
        channels_details_list.append = channel_details_v1(auth_user_id, i)

    # Return the list of channel details
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

