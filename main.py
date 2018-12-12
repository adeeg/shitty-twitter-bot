import tweepy
import json

auth_data = None
with open('auth.json') as f:
    auth_data = json.load(f)
    f.close()

print(auth_data)