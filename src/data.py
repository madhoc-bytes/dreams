import os 
import pickle

# not persistent
if not os.path.isfile('persistent_data.p'):
    users = []
    # example of what users list with 1 user would look like
    '''
    {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'u_id': auth_user_id,
        'token': new_token,
        'permission_id': permission_id,
        'timestamp_ch': 1234,
        'timestamp_dm': 1234,
        'timestamp_msg': 1234,
    }
    '''
    channels = []
    '''
    {   
        'id': 0,
        'is_public': True,
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 0,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'messages': [
            {
                'message_id': 0,
                'u_id': 0,
                'message': 'hello123',
                'time_created': 123123123,
                'reacts': 'reacts',
                'is_pinned': false,
            }
        ],
    }
    '''
    dms = []
    '''
    {   
        'dm_id': 0,
        'dm_name': 'Hayden',
        'owner_id': id
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'messages': [
            {
                'message_id': 0,
                'u_id': 0,
                'message': 'hello123',
                'time_created': 123123123,
                'reacts': 'reacts',
                'is_pinned': false,
            }
        ],
    }
    ''' 
    dreams = {
        'timestamp_ch': 0,
        'timestamp_dm': 0,
        'timestamp_msg': 0,
    }
# persistent
else:
    with open('persistent_data.p', 'rb') as file:
        users = pickle.load(file)
        channels = pickle.load(file)
        dms = pickle.load(file)
        dreams = pickle.load(file)

def persist_data():
    with open('persistent_data.p', 'wb') as file:
        pickle.dump(users, file)
        pickle.dump(channels, file)
        pickle.dump(dms, file)
        pickle.dump(dreams, file)

