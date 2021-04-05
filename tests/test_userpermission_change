# test if the admin_userpermission_change correctly
def test_admin_userpermission_change():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    assert data_permission(1) == 2
    admin_userpermission_change(information_user['token'], 1, 1)
    assert data_permission(1) == 1

def test_admin_userpermission_change_invalid_token():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(AccessError):
        admin_userpermission_change(information_user['token'] + 'a', 1, 1)

def test_admin_userpermission_change_invalid_user():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(InputError):
        admin_userpermission_change(information_user['token'], 3, 1)

def test_admin_userpermission_change_invalid_permission():
    clear_v2()
    information_user = auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(InputError):
        admin_userpermission_change(information_user['token'], 1, 3)

def test_admin_userpermission_change_not_oDuner():
    clear_v2()
    auth_register_v2("dubaida@gmail.com", "xujiawen", "qwer", "Du")
    info2 = auth_register_v2("kendelle@qwef.com", "sdfgwg334", "BDSF", "Kendelle")
    with pytest.raises(AccessError):
        admin_userpermission_change(info2['token'], 0, 2)