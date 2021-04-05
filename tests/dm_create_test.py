import pytest

from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_invite_v1, dm_details_v1, dm_list_v1, dm_messages_v1
from src.error import InputError, AccessError
from src.other import clear_v2


def test_dm_create_basic():    
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']

    #create one user to pass in the list of users for dm create
    invitee_id = auth_register_v2('test_user@gmail.com', 'test_pw_user', 'userf', 'userl')['auth_user_id']

    u_ids = [invitee_id]
    # create a test dm
    dm_data = dm_create_v1(auth_token, u_ids)
    assert(dm_data['dm_id'] == 0 and dm_data['dm_name'] == 'testftestl, userfuserl')

def test_dm_invalid_id():
    clear_v2()

    #owner of dm/caller of dm_create
    auth = auth_register_v2('test_auth@gmail.com', 'test_pw_auth', 'testf', 'testl')
    auth_token = auth['token']
    auth_id = auth['auth_user_id']
    
    #id of user that does not exist
    u_ids = [2]

    with pytest.raises(InputError):
        dm_create_v1(auth_token, u_ids)