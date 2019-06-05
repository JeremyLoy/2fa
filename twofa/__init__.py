import binascii
import pickle
from dataclasses import dataclass
from json import dumps
from pathlib import Path
from typing import Dict

import click
import pyotp
import pyperclip

FILE = Path.home().joinpath(".2fa")

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@dataclass
class Service:
    name: str
    secret: str
    interval: int = 30

    def now(self):
        return pyotp.TOTP(self.secret, interval=self.interval).now()


_services: Dict[str, Service] = {}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--json", "-j", is_flag=True, help="Output all as JSON.")
@click.pass_context
def cli(ctx, json):
    """
    Provides Time-Based One Time Passwords (TOTP) utilities.

    If no arguments given, lists all configured services with their current
    TOTP.

    See RFC 4226 (HOTP) 6238 (TOTP) for more info.
    \f
    :param ctx: the click context.
    :param json: True if output should be JSON, False otherwise.
    """
    load_state()
    if ctx.invoked_subcommand is None:
        print_all(json)


@cli.command()
@click.argument("name", metavar="SERVICE")
@click.option("--interval", "-i", type=int)
def add(name, interval):
    """
    Add a service to this tool.

    Prompts the user for the secret.
    Rejects bad secrets.

    \f
    :param name: The service to add. i.e. github.
    :param interval: The lifetime of an OTP.
    """
    secret = click.prompt("Secret", hide_input=True)
    service = Service(name, secret)

    if interval:
        service.interval = interval

    try:
        service.now()
    except binascii.Error:
        click.echo("Bad secret key.")
        return

    _services[service.name] = service
    click.echo(f"{service.name} added!")
    save_state()


@cli.command()
@click.argument("name", metavar="SERVICE")
def copy(name):
    """
    Copy the current TOTP for SERVICE to the clipboard.
    \f
    :param name: The service to generate a OTP for.
    """
    try:
        service = _services[name]
        pyperclip.copy(service.now())
        click.echo(f"{service.name} was copied to your clipboard!")
    except KeyError:
        click.echo(f"{service.name} does not exist")


@cli.command()
@click.argument("services", nargs=-1)
def remove(services):
    """
    Remove services from this tool.
    \f
    :param services: The services to remove.
    """
    for service in services:
        try:
            _services.pop(service)
            click.echo(f"{service} removed!")
        except KeyError:
            click.echo(f"{service} does not exist")
    save_state()


def save_state():
    with open(FILE, "wb") as f:
        pickle.dump(_services, f)


def load_state():
    try:
        with open(FILE, "rb") as f:
            global _services
            _services = pickle.load(f)
    except FileNotFoundError:
        pass


def print_all(json: bool):
    """
    click.echo all services in JSON format or as a table.
    :param json: True if click.echoing as JSON format
    """
    services = {name: service.now() for name, service in _services.items()}

    if json:
        click.echo(dumps(services))
    else:
        click.echo(table(services))


def table(services: Dict[str, str]) -> str:
    """
    Collect all services and their current otp as a table.
     
    :param services: Dictionary of service name to otp
    :return: the table representation of d as a string
    """
    # the longest service name or 10
    left_column = max([10, *map(len, services)])
    right_column = 8  # max number of digits specified by RFC

    header = f'{"service":<{left_column}} | {"otp":<{right_column}}'

    divider = "-" * len(header)

    body = [
        f"{service:<{left_column}} | {otp:{right_column}}"
        for service, otp in services.items()
    ]

    return "\n".join([header, divider, *body])
