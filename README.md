# shitty-twitter-bot

## Setup

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
* change `MSG_REPLY` in `main.py` to what you want
* add some users in `users.json` e.g.
    ```
    {"xxxxxxx": 1, "xxxxxxy": 1}
    ```
    * where `xxxxxxx` is the user's id ([use this](http://gettwitterid.com/))
    * if a user opts out **do not** add them back

## Running

1. `pip install -r requirements.txt`
2. `python3 main.py`

## About

Tweets from users will be replied to with a given message.

To opt out, tweet the bot '@[bot_handle] opt-out'

Opting in does not work because you can only have one stream per bot >:(

Code probably bad and easy to break

Sorry if this is against Twitter's rules I'll remove if so!