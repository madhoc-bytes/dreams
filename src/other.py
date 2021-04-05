from src.data import users, channels

''' Resets the internal data of the application to it's initial state '''
def clear_v2():
    users.clear()
    channels.clear()
    return {}

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

''' create len of channels to check if clear'''
def data_channels():
    return len(channels)
''' create len of users to check if clear'''
def data_user():
    return len(users)
