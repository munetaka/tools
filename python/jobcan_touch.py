import requests

from util import is_weekend_or_holiday


def main():
    # https://api.slack.com/legacy/custom-integrations/legacy-tokens
    token = ''
    channel = ''  # DM Slackbot

    if is_weekend_or_holiday():
        print('today is non-working day')
        exit()

    url = 'https://slack.com/api/chat.command'
    command = '/jobcan_touch'
    params = {
        'token': token,
        'channel': channel,
        'command': command,
    }
    res = requests.post(url, params=params)
    print(res.text)


if __name__ == '__main__':
    main()
