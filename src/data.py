import os 
import pickle

# not persistent
if not os.path.isfile('persistent_data.p'):
    users = []
    # example of what users list with 1 user would look like
    '''
    {
        'email': 'emai@email.com',
        'password': 'Password1',
        'name_first': 'user',
        'name_last': 'name',
        'handle': 'username',
        'u_id': 0,
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
                'message_string': 'hello123',
                'time': 123123123,
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
                'message_string': 'hello123',
                'time': 123123123,
            }
        ],
    }
    '''
# persistent
else:
    with open('persistent_data.p', 'rb') as file:
        users = pickle.load(file)
        channels = pickle.load(file)
        dms = pickle.load(file)

def persist_data():
    with open('persistent_data.p', 'wb') as file:
        pickle.dump(users, file)
        pickle.dump(channels, file)
        pickle.dump(dms, file)

