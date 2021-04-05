import pytest
from src.auth import auth_register_v2
from src.other import clear_v2
from src.error import InputError, AccessError
from src.admin_userpermission_change_v1 import adminuserpermissionchangev1, change_permission

# test if the adminuserpermissionchangev1 correctly
def test_adminuserpermissionchangev1_invalid_token():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(AccessError):
        adminuserpermissionchangev1(information_user['token'] + 'a', 1, 1)

def test_adminuserpermissionchangev1_invalid_permission():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(InputError):
        adminuserpermissionchangev1(information_user['token'], 1, 3)
