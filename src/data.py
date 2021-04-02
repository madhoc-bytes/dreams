users = []
'''
{
    'email': 'emai@email.com',
    'password': 'Password1',
    'name_first': 'user',
    'name_last': 'name',
    'handle': 'username',
    'u_id': 0,
    'token': 0,
    'permission_id': 0
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
	    'is_public': True,
	    'dm_name': 'Hayden',
	    'all_dm_members': [
	        {
	            'dm_id': 0,
	            'name_first': 'Hayden',
	            'name_last': 'Jacobs',
	        }
	    ],
	}
'''


notifications = []
    {
        'channel_id': 0,
        'dm_id': 0
        'notifications_message': 'You have a new message'
    }