# For slack notify
import json
import requests
import socket

def slack_notify(webhook_url,channel_name,title,
                 message,subtitle='',emoji=':computer:'):
    """
    A function which sends a slack notification

    Based in part on:
    https://www.amphioxus.org/content/slack-notifications-scripts#python
    https://www.webpagefx.com/tools/emoji-cheat-sheet/ , and
    https://github.com/sulhome/bash-slack
    """

    # Formulate message
    if subtitle!='':
        msgdata={
            "channel": channel_name,
            "username": socket.gethostname(),
            "icon_emoji": emoji,
            "attachments": [
                {
                    "fallback": title,
                    "color": "good",
                    "title": title,
                    "fields": [{
                        "title": subtitle,
                        "value": message,
                        "short": False
                    }]
                }
            ]
        }
    else:
        msgdata={
            "channel": channel_name,
            "username": socket.gethostname(),
            "icon_emoji": emoji,
            "attachments": [
                {
                    "fallback": title,
                    "color": "good",
                    "title": title,
                    "fields": [{
                        "value": message,
                        "short": False
                    }]
                }
            ]
        }
    
    # Contact slack
    response=requests.post(webhook_url,data=json.dumps(msgdata),
                           headers={'Content-Type': 'application/json'}
    )

    # If error is returned
    if response.status_code!=200:
        str_temp=('Request to Slack returned '+
                  'error:\n{}. Response is:\n{}')
        raise ValueError(str_temp.format(response.status_code,
                                         response.text))
    
