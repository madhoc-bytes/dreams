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
        'num_channels_joined': 0,
        'num_dms_joined': 0,
        'num_messages_sent': 0,
        'timestamp_ch': [
            {
                'num_channels_joined': 0,
                'time_stamp': 123
            },
            {
                'num_channels_joined': 1,
                'time_stamp': 130
            }
        ],
        'timestamp_dm': [
            {
                'num_dms_joined': 0,
                'time_stamp': 123
            },
            {
                'num_dms_joined': 1,
                'time_stamp': 130
            }
        ],
        'timestamp_msg': [
            {
                'num_messages_sent': 0,
                'time_stamp': 123
            },
            {
                'num_messages_sent': 1,
                'time_stamp': 130
            }
        ],
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
    dreams = {}
    # example of what dreams stats dict would look like 
    '''
    'channels': 1,
    'dms': 1,
    'msgs': 0,
    'timestamp_ch': [
        {
            'num_channels_exist': 0, 
            'time_stamp': 123
        },
        {
            'num_channels_exist': 1, 
            'time_stamp': 125
        }
    ],
    'timestamp_dm': [
        {
            'num_dms_exist': 0, 
            'time_stamp': 123
        },
        {
            'num_dms_exist': 1, 
            'time_stamp': 125
        }
    ],
    'timestamp_msg': [
        {
            'num_messages_exist': 0, 
            'time_stamp': 123
        },
        {
            'num_messages_exist': 1, 
            'time_stamp': 125
        }
    ]
    '''
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
