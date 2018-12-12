import tweepy
import json

auth_data = None
with open('auth.json') as f:
    auth_data = json.load(f)
    f.close()

cons_key = auth_data['consumer_key']
cons_sec = auth_data['consumer_secret']
acc_tok = auth_data['access_token']
acc_tok_sec = auth_data['access_token_secret']

auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(acc_tok, acc_tok_sec)
api = tweepy.API(auth)

user = api.me()
print(user.name)

# get opt-in from user