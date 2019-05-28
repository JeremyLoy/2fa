import click
from json import dumps
import pyotp
import pyperclip
import pickle
from pathlib import Path

FILE = Path.home().joinpath('.2fa')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

data = {}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('--json', '-j', is_flag=True, help='Output all as JSON.')
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
@click.argument('service')
@click.argument('secret')
def add(service, secret):
    """
    Add a service to this tool.

    \f
    :param service: The service to add. i.e. github.
    :param secret:  The secret used to derive the OTP.
    """
    # TODO validate key length
    data[service] = secret
    print(f'{service} added!')
    save_state()


@cli.command()
@click.argument('service')
def copy(service):
    """
    Copy the current TOTP for SERVICE to the clipboard.
    \f
    :param service: The service to generate a OTP for.
    """
    try:
        otp = pyotp.TOTP(data[service]).now()
        pyperclip.copy(otp)
        print(f'{service} was copied to your clipboard!')
    except KeyError:
        print(f'{service} does not exist')


@cli.command()
@click.argument('services', nargs=-1)
def remove(services):
    """
    Remove services from this tool.
    \f
    :param services: The services to remove.
    """
    for service in services:
        try:
            data.pop(service)
            print(f'{service} removed!')
        except KeyError:
            print(f'{service} does not exist')
    save_state()


def save_state():
    with open(FILE, 'wb') as f:
        pickle.dump(data, f)


def load_state():
    try:
        with open(FILE, 'rb') as f:
            global data
            data = pickle.load(f)
    except FileNotFoundError:
        pass


def print_all(json):
    d = {service: pyotp.TOTP(secret).now()
         for service, secret in data.items()}

    if json:
        print(dumps(d))
    else:
        print_all_table(d)


def print_all_table(d):
    left_column = len(max(d)) if d else 10  # the longest service name or 10
    right_column = 8  # max number of digits specified by RFC

    header = f'{"service":<{left_column}} | {"otp":<{right_column}}'

    print(header)
    print('-' * len(header))
    for service, otp in d.items():
        print(f'{service:<{left_column}} | {otp:{right_column}}')
