# shitty-twitter-bot

## Running

* make sure the twitter account for your bot can receive direct messages
* get API keys for your [bot](developer.twitter.com)
* create & fill in `auth.json`

```
{
    "twitter_handle": "",
    "consumer_key": "",
    "consumer_secret": "",
    "access_token": "",
    "access_token_secret": ""
}
```

* `pip install -r requirements.txt`
* `python3 main.py`

## Using

Tweets from users (in users.txt) will be replied to with a given message.

To opt out, tweet the bot '@nenivar, I would like to opt-out!'

Opting in does not work because you can only have one stream per bot >:(