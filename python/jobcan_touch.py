import requests

from util import is_weekend_or_holiday


def main():
    # https://api.slack.com/legacy/custom-integrations/legacy-tokens
    token = ''
    url = 'https://slack.com/api/chat.command'
    channel = ''  # DM Slackbot

    if is_weekend_or_holiday():
        text = 'today is non-working day'
        params = {
            'token': token,
            'channel': channel,
            # 'command': command,
            'text': text,
        }
    else:
        # command = '/jobcan_touch'
        text = 'today is working day'
        params = {
            'token': token,
            'channel': channel,
            # 'command': command,
            'text': text,
        }

    res = requests.post(url, params=params)
    print(res)


if __name__ == '__main__':
    main()
