1. If an user is invited to the channel with channel_invite_v1(), they are inserted automatically regardless of whether the channel was public or private
2. channel_invite_v1() doesn't check if auth_user has permission to do so (if auth_user is an admin/owner)
3. channel_invite_v1() assumes that a user with auth_user_id already exists
4. channel_details_v1() will always return a dictionary with an empty list of 'owner_members' as it is not specified in this iteration