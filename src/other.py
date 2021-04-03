from src.data import users, channels
from src.channel import test_user_is_invalid
from src.error import InputError, AccessError

''' Resets the internal data of the application to it's initial state '''
def clear_v1():
    users.clear()
    channels.clear()

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