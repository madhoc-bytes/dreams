''' Test file for dm_invite_v1 '''

import pytest 
from src.dm_invite_v1 import dm_invite_v1, is_user_in_dm
from src.error import InputError, AccessError
from src.data import users, dms
from src.dm_create_v2 import dm_create_v1
from src.other import clear_v2
from src.auth import auth_register_v2

def test_dm_invite():
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    user_id_1 = auth_register_v2('test132@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']
    user_id_2 = auth_register_v2('test@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']

    dm_id = dm_create_v1(token, user_id_1)['dm_id']
    dm_invite_v1(token, dm_id, user_id_1)

    assert is_user_in_dm(user_id_1, dm_id) == True

def test_dm_invite_invalid_dm():
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    user_id_1 = auth_register_v2('test132@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']
    user_id_2 = auth_register_v2('test@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']

    dm_id = 12

    with pytest.raises(InputError):
        dm_invite_v1(token, dm_id, user_id_1)

def test_dm_invite_invalid_user():
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    user_id_1 = 14
    user_id_2 = auth_register_v2('test@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']

    dm_id = dm_create_v1(token, user_id_2)['dm_id']

    with pytest.raises(InputError):
        dm_invite_v1(token, dm_id, user_id_1)


def test_dm_invite_user_already_in_dm():
    clear_v2()

    token = auth_register_v2('germanijack@yahoo.com', 'jack123', 'Jack', 'Germani')['token']
    user_id_1 = auth_register_v2('test132@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']
    user_id_2 = auth_register_v2('test@yahoo.com', 'test123', 'Test', 'Test')['auth_user_id']

    dm_id = dm_create_v1(token, user_id_1)['dm_id']
    dm_invite_v1(token, dm_id, user_id_1)

    with pytest.raises(AccessError):
        dm_invite_v1(token, dm_id, user_id_1)


