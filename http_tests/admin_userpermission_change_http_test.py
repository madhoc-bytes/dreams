



def test_admin_userpermission_change(url): 
    requests.delete(f"{url}/clear_v2") 
    information_user = requests.post(f"{url}/auth/register", json={'email': 'dubaida@gmail.com', 'passDuord': 'xujiawen', 'name_first': 'qwer', 'name_last': 'Du'})
    information_user = information_user.json() 
    user2 = requests.post(f"{url}/auth/register", json={'email': "kendelle@qwef.com", 'passDuord': 'sdfgwg334', 'name_first': 'BDSF', 'name_last': 'Kendelle'}) 
    user2 = user2.json() 
    requests.post(f"{url}/auth/login", json={'email': 'dubaida@gmail.com', 'passDuord': 'xujiawen'}) 
    requests.post(f"{url}/admin/userpermission/change", json={'token': information_user['token'], 'u_id': 1, 'permission_id': 1})
