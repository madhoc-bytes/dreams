1. channel_messages_v1 is always given a positive integer for 'start'
2. The list of messages returned from channel_messages_v1 is always empty as there isn;t a way to send messages yet
3. channel_join_v1 assumes that the given user exists in ther users dictionary
4. If an user is invited to the channel with channel_invite_v1(), they are inserted automatically regardless of whether the channel was public or private
5. channel_invite_v1() doesn't check if auth_user has permission to do so (if auth_user is an admin/owner)
6. channel_invite_v1() assumes that a user with auth_user_id already exists
7. channel_details_v1() will always return a dictionary with an empty list of 'owner_members' as it is not specified in this iteration
