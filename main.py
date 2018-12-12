import tweepy
import json
from threading import Lock

"""
    read in auth data
"""

auth_data = None
with open('auth.json') as f:
    auth_data = json.load(f)
    f.close()

handle = auth_data['twitter_handle']
cons_key = auth_data['consumer_key']
cons_sec = auth_data['consumer_secret']
acc_tok = auth_data['access_token']
acc_tok_sec = auth_data['access_token_secret']

MSG_OPT_IN = '@{}, I would like to opt-in!'.format(handle)
MSG_OPT_OUT = '@{}, I would like to opt-out!'.format(handle)
MSG_AT = '@{}'.format(handle)
MSG_REPLY = 'Here\'s your custom message!'

"""
    get opt-in from user
    & opt-out
"""
users = []

# read in existing users
with open('users.txt', 'r') as f:
    for x in f.readlines():
        users.append(x.strip())
    f.close()

def addUserToFile(userId):
    with open('users.txt', 'a') as f:
        f.write('{}\n'.format(userId))
        f.close()

def removeUserFromFile(userId):
    new = []
    with open('users.txt', 'r') as f:
        lines = f.readlines()
        new = list(filter(lambda x: x != userId, users))
        f.close()
    with open('users.txt', 'w') as f:
        f.writelines(new)
        f.close()

def addUser(userId):
    if userId not in users:
        addUserToFile(userId)
        users.append(userId)

def removeUser(userId):
    if userId in users:
        removeUserFromFile(userId)
        users.remove(userId)

"""
    tweepy stuff
"""
auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(acc_tok, acc_tok_sec)
api = tweepy.API(auth)

user = api.me()
print('Bot running on {}'.format(user.name))

class StreamBoth(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.restart = False

    def on_connect(self):
        print('Streaming started with users {}'.format(users))
    
    def on_status(self, status):
        # for user opting in/out
        if MSG_AT in status.text:
            print('{} tweeted you!'.format(status.user.name))
            if status.text == MSG_OPT_IN:
                print('{} opted in!'.format(status.user.name))
                addUser(user)
                self.restart = True
            elif status.text == MSG_OPT_OUT:
                print('{} opted out!'.format(status.user.name))
                removeUser(user)
                self.restart = True
        # for tracked user tweeting
        elif status.user.id_str in users:
            print('Tweeted @{}'.format(status.user.name))
            api.update_status('@{} {}'.format(status.user.name, MSG_REPLY))

streamList = StreamBoth()
stream = tweepy.Stream(auth = api.auth, listener=streamList)
stream.filter(track=MSG_AT, follow=users, is_async=True)

while 1:
    if streamList.restart:
        print('User opted in/out; restarting...')
        stream.disconnect()

        # restart with new set of users
        stream = StreamBoth()
        stream = tweepy.Stream(auth = api.auth, listener=streamList)
        stream.filter(track=MSG_AT, follow=users, is_async=True)