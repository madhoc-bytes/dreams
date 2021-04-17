from src.channel import test_channel_is_invalid, test_if_user_in_ch, token_to_id
from src.data import channels, users
from src.error import InputError, AccessError
from src.message import message_send_v1
import datetime
import threading
import json

def standup_start_v1(token, channel_id, length):
   # change the token to a u id
    auth_user_id = token_to_id(token)
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()
    # invalid user
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()
    #channel get.
    standupchannel = channelid_to_channel(channel_id)
    #get now time
    now = datetime.datetime.utcnow()
    timesymbol = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    #find the difference time
    difference = standupchannel['standup']['finishtime'] - timesymbol
     # no active standup is runing in the given channel
    if difference <= 0:
        raise InputError()

    #clear all the message
    nonemessage(channel_id)

    #last_time = datetime.datetime.strptime(f_time,'%Y-%m-%d %H:%M:%S')
    timefinishsend = timesymbol + length
    finishtime(channel_id, timefinishsend)

    threading.Timer(length, sendmessagestart(token, channel_id)).start()

    return {
        'time_finish': timefinishsend,
    }

#standup_active
def standup_active_v1(token, channel_id):
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()
    #channel get.
    standupchannel = channelid_to_channel(channel_id)
    #get now time
    now = datetime.datetime.utcnow()
    timesymbol = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    #find the difference time
    difference = standupchannel['standup']['finishtime'] - timesymbol

    if difference > 0:
        is_active = True
        time_finish = standupchannel['standup']['finishtime']
    else:
        is_active = False
        time_finish = None

    return {
        'is_active': is_active,
        'time_finish': time_finish,
    }

def standup_send_v1(token, channel_id, message):
    # change the token to a u id
    auth_user_id = token_to_id(token)
    # invalid channel
    if test_channel_is_invalid(channel_id):
        raise InputError()
    # invalid user
    if not test_if_user_in_ch(auth_user_id, channel_id):
        raise AccessError()
    # invalid message
    if len(message) > 1000:                
        raise InputError()
    #channel get.
    standupchannel = channelid_to_channel(channel_id)
    #get now time
    now = datetime.datetime.utcnow()
    timesymbol = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    #find the difference time
    difference = standupchannel['standup']['finishtime'] - timesymbol
     # no active standup is runing in the given channel
    if difference <= 0:
        raise InputError()
    
    userfirstname = token_to_name(token)
    send_message = userfirstname + '-> ' + message + '\n'
    addmessage(channel_id, send_message)

    return {}
############
############
############
# helper function
def channelid_to_channel(channel_id):
    channelneed = None
    for item in channels:
        if item['channel_id'] == channel_id:
            channelneed = item
            break
    return channelneed

def token_to_name(token):
    if len(users) == 0:
        return ''
    for user in users:
        key, value = 'token', token
        if key in user and value == user[key]:
            return user['name_first']
    return -1
#send message start
def sendmessagestart(token, channel_id):
    send_message = channelid_to_channel(channel_id)['standup']['messagesend_pack']
    message_send_v1(token, channel_id, send_message)

def finishtime(channel_id, timefinish):
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #channel_id
    for item in channels:
        if item['channel_id'] == channel_id:
            #change the value
            item['standup']['finishtime'] = timefinish

    # json
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def addmessage(channel_id, message):
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #channel_id
    for item in channels:
        if item['channel_id'] == channel_id:
            item['standup']['messagesend_pack'] += message

    # json
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

def nonemessage(channel_id):
    with open('src/data/channels.json', 'r') as file:
        channels = json.load(file)

    #channel_id
    for item in channels:
        if item['channel_id'] == channel_id:
            item['standup']['messagesend_pack'] = ''

    # json
    with open('src/data/channels.json', 'w') as file:
        json.dump(channels, file)

