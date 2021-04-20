import pytest

from src.auth import auth_register_v2
from src.users import users_all_v1
from src.other import clear_v2

def test_system():
    clear_v2()
    # register 1 user
    user1 = auth_register_v2(
        'test_email1@gmail.com',
        'test_pw1',
        'test_fname1',
        'test_lname1'
    )
    assert users_all_v1(user1['token']) == {
        'users' : [
            {
                'u_id': user1['auth_user_id'],
                'email': 'test_email1@gmail.com',
                'name_first': 'test_fname1',
                'name_last': 'test_lname1',
                'handle_str': 'test_fname1test_lname1',
                'profile_img_url': ''
            }
        ]
    }

    # register 2 more users
    user2 = auth_register_v2(
        'test_email2@gmail.com',
        'test_pw2',
        'test_fname2',
        'test_lname2'
    )
    user3 = auth_register_v2(
        'test_email3@gmail.com',
        'test_pw3',
        'test_fname3',
        'test_lname3'
    )
    assert users_all_v1(user1['token']) == {
        'users': [
            {
                'u_id': user1['auth_user_id'],
                'email': 'test_email1@gmail.com',
                'name_first': 'test_fname1',
                'name_last': 'test_lname1',
                'handle_str': 'test_fname1test_lname1',
                'profile_img_url': ''
            },
            {
                'u_id': user2['auth_user_id'],
                'email': 'test_email2@gmail.com',
                'name_first': 'test_fname2',
                'name_last': 'test_lname2',
                'handle_str': 'test_fname2test_lname2',
                'profile_img_url': ''
            },
            {
                'u_id': user3['auth_user_id'],
                'email': 'test_email3@gmail.com',
                'name_first': 'test_fname3',
                'name_last': 'test_lname3',
                'handle_str': 'test_fname3test_lname3',
                'profile_img_url': ''
            },
        ]
    }
