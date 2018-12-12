import tweepy
import json
import os.path

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

MSG_OPT_IN = 'opt-in'
MSG_OPT_OUT = 'opt-out'
MSG_AT = '@{}'.format(handle)
MSG_REPLY = 'Here\'s your custom message!'

"""
    get opt-in from user
    & opt-out
"""
FILE_USERS = 'users.json'
users = {}

# read in existing users
def readUsersFromFile() -> {}:
    users = {}
    if os.path.isfile(FILE_USERS):
        with open(FILE_USERS, 'r') as f:
            users = json.load(f)
            f.close()
    return users

def saveUsersToFile() -> None:
    with open(FILE_USERS, 'w') as f:
        json.dump(users, f)
        f.close()

def addUser(userId: str) -> None:
    users[userId] = 0
    saveUsersToFile()

def removeUser(userId: str) -> None:
    if userId in users:
        users.pop(userId)    
        saveUsersToFile()

def incUserSent(userId: str) -> None:
    if userId in users:
        users[userId] += 1
        saveUsersToFile()

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
        print('Streaming started with users {}'.format(list(users.keys())))
    
    def on_status(self, status):
        # for user opting in/out
        if MSG_AT in status.text:
            print('{} tweeted you!'.format(status.user.screen_name))
            if MSG_OPT_IN in status.text:
                print('{} opted in!'.format(status.user.screen_name))
                addUser(status.user.id_str)
                self.restart = True
            elif MSG_OPT_OUT in status.text:
                print('{} opted out!'.format(status.user.screen_name))
                removeUser(status.user.id_str)
                self.restart = True
        # for tracked user tweeting
        elif status.user.id_str in list(users.keys()):
            print('Tweeted @{}'.format(status.user.screen_name))
            api.update_status('@{} {} #{}'.format(status.user.screen_name, MSG_REPLY, users[status.user.id_str]), status.id_str)
            incUserSent(status.user.id_str)

"""
    let's do stuff
"""
users = readUsersFromFile()
if not users:
    print('No users in users.json!')

streamList = StreamBoth()
stream = tweepy.Stream(auth = api.auth, listener=streamList)
stream.filter(track=MSG_AT, follow=users, is_async=True)

while True:
    if streamList.restart:
        print('User opted in/out; restarting...')
        stream.disconnect()

        # restart with new set of users
        streamList = StreamBoth()
        stream = tweepy.Stream(auth = api.auth, listener=streamList)
        stream.filter(track=MSG_AT, follow=users, is_async=True)