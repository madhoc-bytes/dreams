''' '''

List of dictionaries, where each dictionary contains types { channel_id, dm_id, notification_message } where channel_id is the 
id of the channel that the event happened in, and is -1 if it is being sent to a DM. dm_id is the DM that the event happened in, 
and is -1 if it is being sent to a channel. 

The list should be ordered from most to least recent. Notification_message is a string 
of the following format for each trigger action:   

from src.data import users, channels


# Return the user's most recent 20 notifications
def notifications_get_v1(auth_user_id):
    


    return { }
    
