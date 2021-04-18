from src.data import users, channels, dms, dreams
from src.channel import token_to_id

def users_all_v1(token):
    users_list = []

    for user in users:
        new_user = {
            'u_id': user['u_id'], 
            'email': user['email'], 
            'name_first': user['name_first'], 
            'name_last': user['name_last'], 
            'handle_str': user['handle']
        }
        users_list.append(new_user)

    return {'users': users_list}

def users_stats_v1(token):
    num_users_with_involvement = 0
    for user in users:
        if len(user['timestamp_ch']) + len(user['timestamp_dm']) > 0:
            num_users_with_involvement += 1    

    return {
        'dreams_stats' : {
            'channels_exist': dreams['timestamp_ch'],
            'dms_exist': dreams['timestamp_dm'],
            'messages_exist': dreams['timestamp_msg'],
            'utilization_rate': num_users_with_involvement / len(users)
        }
    }