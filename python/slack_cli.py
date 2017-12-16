import click
import requests


@click.group()
def cli():
    pass


def get_channel_list(token):
    url = 'https://slack.com/api/channels.list'
    data = {
        'token': token
    }
    response = requests.post(
        url,
        data=data
    )
    return response.json().get('channels')


def get_channel_history(token, channel_id, count=100):
    url = 'https://slack.com/api/channels.history'
    data = {
        'token': token,
        'channel': channel_id,
        'count': count
    }
    response = requests.post(
        url,
        data=data
    )
    return response.json().get('messages')


def delete_message(token, channel_id, timestamp):
    url = 'https://slack.com/api/chat.delete'
    data = {
        'token': token,
        'channel': channel_id,
        'ts': timestamp
    }

    return requests.post(
        url,
        data=data
    )


@cli.command()
@click.argument('token', required=True)
@click.argument('channel', required=True)
@click.option('--force', '-f', is_flag=True, default=False)
def channel_info(token, channel, force):
    channel_list = get_channel_list(token)
    for channel_info in channel_list:
        if channel_info.get('name') == channel:
            click.echo(channel_info)


@cli.command()
@click.argument('token', required=True)
@click.argument('channel', required=True)
@click.option('--force', '-f', is_flag=True, default=False)
def channel_history(token, channel, force):
    channel_list = get_channel_list(token)
    for channel_info in channel_list:
        if channel_info.get('name') == channel:
            channel_id = channel_info.get('id')
            break

    history = get_channel_history(token, channel_id)
    for message in history:
        print(message)


@cli.command()
@click.argument('token', required=True)
@click.argument('channel', required=True)
@click.argument('count', type=int, default=1)
@click.option('--force', '-f', is_flag=True, default=False)
def delete_messages(token, channel, count, force):
    channel_list = get_channel_list(token)
    for channel_info in channel_list:
        if channel_info.get('name') == channel:
            channel_id = channel_info.get('id')
            break

    history = get_channel_history(token, channel_id, count)
    for message in history:
        click.echo(message)
        if force is True:
            response = delete_message(token, channel_id, message.get('ts'))
            if response.json().get('ok') is True:
                click.echo('<success> delete {}. ts = {}'.format(message.get('type'), message.get('ts')))
            else:
                click.echo('<fail> delete {}. ts = {}'.format(message.get('type'), message.get('ts')))
        else:
            click.echo('<dry-run> delete {}. ts = {}'.format(message.get('type'), message.get('ts')))


def main():
    cli()


if __name__ == '__main__':
    main()
