import base64
import hashlib
import hmac
import json
import os
import time
import uuid
from enum import Enum, auto

import requests
import typer

Response = requests.models.Response

app = typer.Typer()


class RequestMethod(Enum):
    GET = auto()
    POST = auto()


def _make_headers() -> dict[str, str]:
    token = os.environ["SWITCHBOT_TOKEN"]
    secret = os.environ["SWITCHBOT_SECRET"]
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)

    sign = base64.b64encode(
        hmac.new(
            bytes(secret, "utf-8"),
            msg=bytes(string_to_sign, "utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
    )

    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "charset": "utf8",
        "t": str(t),
        "sign": str(sign, "utf-8"),
        "nonce": str(nonce),
    }


def _send_request(url: str, method: RequestMethod, data: dict = {}) -> dict:
    res: Response
    if method == RequestMethod.GET:
        res = _send_get_request(url)
    elif method == RequestMethod.POST:
        res = _send_post_request(url, data)

    if res.status_code != 200:
        typer.echo(
            f"got http request error.\nstatus code: {res.status_code}",
            err=True,
        )
        exit()

    res_json = res.json()

    if res_json.get("statusCode") != 100:
        typer.echo(
            f"got api request error.\nerror message: {res_json.get('message')}\nstatus code is {res_json.get('statusCode')}",
            err=True,
        )
        exit()

    return res_json.get("body")


def _send_get_request(url: str) -> Response:
    return requests.get(
        url,
        headers=_make_headers(),
    )


def _send_post_request(url: str, data: dict) -> Response:
    return requests.post(
        url,
        data=json.dumps(data),
        headers=_make_headers(),
    )


def _device_on(device_id: str) -> None:
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    data = {"command": "turnOn", "parameter": "default", "commandType": "command"}
    _send_request(url, method=RequestMethod.POST, data=data)


def _device_off(device_id: str) -> None:
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    data = {"command": "turnOff", "parameter": "default", "commandType": "command"}
    _send_request(url, method=RequestMethod.POST, data=data)


def _get_device_status(device_id: str) -> dict:
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    return _send_request(url, method=RequestMethod.GET)


def _get_device_list() -> list[dict]:
    url = "https://api.switch-bot.com/v1.1/devices"
    res_json: dict = _send_request(url, method=RequestMethod.GET)

    return res_json.get("deviceList", [])


@app.command()
def hello(
    count: int = typer.Option(1, "-C", "--count", help="Number of greetings."),
    name: str = typer.Option(..., prompt="Your Name", help="The person to greet."),
) -> None:
    """COUNTで与えた回数だけHelloする"""
    for x in range(count):
        typer.echo(f"Hello {name}")


@app.command()
def device_list() -> None:
    device_list: list[dict] = _get_device_list()
    for device in device_list:
        typer.echo("===========================")
        typer.secho(f"deviceName: {device.get('deviceName')}", fg=typer.colors.MAGENTA)
        typer.echo(f"deviceId: {device.get('deviceId')}")
        typer.echo(f"deviceType: {device.get('deviceType')}")


@app.command()
def device_on(device_id: str = typer.Argument(...)) -> None:
    _device_on(device_id)
    typer.echo("on")


@app.command()
def device_off(device_id: str = typer.Argument(...)) -> None:
    _device_off(device_id)
    typer.echo("off")


@app.command()
def device_reboot(device_id: str = typer.Argument(...)) -> None:
    _device_off(device_id)
    time.sleep(5)
    _device_on(device_id)
    typer.echo(typer.style("reboot done", fg="green", bg="red"))


@app.command()
def device_status(device_id: str = typer.Argument(...)) -> None:
    status = _get_device_status(device_id)
    for key, value in status.items():
        typer.echo(f'{key}: {value}')


if __name__ == "__main__":
    app()
