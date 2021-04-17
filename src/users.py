from src.data import users, channels, dms

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
    pass

def num_dreams_msgs():
    total = 0
    for channel in channels:
        total += len(channel['messages'])
    for dm in dms:
        total += len(dm['messages'])
    return total

def num_dreams_channels():
    return len(channels)

def num_dreams_dms():
    return len(dms)