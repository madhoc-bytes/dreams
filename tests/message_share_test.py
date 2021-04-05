'''Test file for message_share_v1.py'''

# Imports
import pytest
from src.data import channels, users, dms
from src.dm_create_v2 import dm_create_v1
from src.dm_invite_v1 import dm_invite_v1
from src.message import message_send_v1, message_share_v1, is_message_shared, message_exists
from src.message_senddm_v2 import message_senddm_v2
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v2
from src.error import InputError, AccessError

# Test user sharing to channel in which he didn't join
def test_message_share_not_authorised_to_channel():
    # Reset
    clear_v2()
    dm_id = -1
    message = ''

    # Create user
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    # Create 2 channels
    channel0 = channels_create_v2(token, 'My Channel', True)
    channel1 = channels_create_v2(token, 'My Channel 2', True)

    # Join user in both channels
    channel_join_v2(token, channel0['channel_id'])

    # Create one messsage
    message_one = 'I am message #1'

    # Send message to channel 1
    og_message_id = message_send_v1(token, channel0, message_one)

    # AccessError
    with pytest.raises(AccessError):
        message_share_v1(token, og_message_id, message, channel1, dm_id)

# Test sharing one message to a channel
def test_message_share_one_message_to_channel():
    # Reset
    clear_v2()
    dm_id = -1
    message = ''

    # Create user
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    # Create 2 channels
    channel0 = channels_create_v2(token, 'My Channel', True)
    channel1 = channels_create_v2(token, 'My Channel 2', True)
    channel2 = channels_create_v2(token, 'My Channel 3', True)

    # Join user in both channels
    channel_join_v2(token, channel0['channel_id'])
    channel_join_v2(token, channel1['channel_id'])

    # Create one messsage
    message_one = 'I am message #1'

    # Send message to channel 1
    og_message_id = message_send_v1(token, channel0, message_one)

    # Share message to channel 2
    first_share_id = message_share_v1(token, og_message_id, message, channel1, dm_id)
    sharing_id = first_share_id['shared_message_id']

    # Make sure it is shared
    result = is_message_shared(sharing_id, channel1)
    
    assert result == True and first_share_id == {'shared_message_id': {'message_id': 2}}

# Test sharing two messages to channels
def test_message_share_two_messages_to_channel():
    # Reset
    clear_v2()
    dm_id = -1
    message = ''

    # Create user
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    token_2 = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['token']

    # Create 2 channels
    channel0 = channels_create_v2(token, 'My Channel', True)
    channel1 = channels_create_v2(token, 'My Channel 2', True)
    channel2 = channels_create_v2(token, 'My Channel 3', True)

    # Join users in all channels
    channel_join_v2(token, channel0['channel_id'])
    channel_join_v2(token, channel1['channel_id'])
    channel_join_v2(token, channel2['channel_id'])
    channel_join_v2(token_2, channel0['channel_id'])
    channel_join_v2(token_2, channel1['channel_id'])
    channel_join_v2(token_2, channel2['channel_id'])

    # Create one messsage
    message_one = 'I am message #1'
    message_two = 'Hello!'
    message_three = 'Goodbye!'

    # Send messages
    message_one_id = message_send_v1(token, channel0, message_one) 
    message_two_id = message_send_v1(token, channel1, message_two) 
    message_three_id = message_send_v1(token, channel2, message_three) 

    # Share messages
    first_share_id = message_share_v1(token, message_one_id, message, channel1, dm_id) 
    second_share_id = message_share_v1(token_2, message_three_id, message, channel0, dm_id)

    sharing_id_1 = first_share_id['shared_message_id']
    sharing_id_2 = second_share_id['shared_message_id']

    # Make sure it is shared
    result_1 = is_message_shared(sharing_id_1, channel1)
    result_2 = is_message_shared(sharing_id_2, channel0)
    
    assert result_1 == True and result_2 == True and first_share_id == {'shared_message_id': {'message_id': 4}} and second_share_id == {'shared_message_id': {'message_id': 5}}

'''
# Test sharing one message to DM: still doesn't work, missing teammates functions
def test_share_message_to_dm():

    clear_v2()
    channel_id = -1
    message = ''

    # Create user
    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    user_id = auth_register_v2('test@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']
    user_id_2 = auth_register_v2('test123@yahoo.com', 'jack123', 'Jack', 'Germani')['auth_user_id']

    # Create 1 dm
    dm_id = dm_create_v1(token, user_id_2)

    # Join user in both channels
    dm_invite_v1(token, dm_id, user_id)

    # Create one messsage
    message_one = 'I am message #1'

    # Send message to channel 1
    og_message_id = message_senddm_v2(token, dm_id, message_one)

    # Share message to channel 2
    first_share_id = message_share_v1(token, og_message_id, message, channel_id, dm_id)
    sharing_id = first_share_id['shared_message_id']

    # Make sure it is shared
    result = is_message_shared(sharing_id, channel1)
    
    assert result == True and first_share_id == {'shared_message_id': {'message_id': 2}}
'''