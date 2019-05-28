import click
import pyotp
import pyperclip
import pickle
from pathlib import Path

FILE = Path.home().joinpath('.2fa')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

data = {}


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Provides Time-Based One Time Passwords (TOTP) utilities.

    If no arguments given, lists all configured services with their current TOTP.

    See RFC 4226 (HOTP) 6238 (TOTP) for more info.
    \f
    :param: ctx
    """
    load_state()
    if ctx.invoked_subcommand is None:
        list_all()


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
    Copy a TOTP to the clipboard.
    \f
    :param service:
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
    :param services:
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


def list_all():
    left_column = max(10, len(max(data.keys()))) # the greater of the longest service name or 10.
    right_column = 8 # max number of digits specified by RFC

    header = f'{"service":<{left_column}} | {"otp":<{right_column}}'

    print(header)
    print('-' * len(header))
    for service, secret in data.items():
        otp = pyotp.TOTP(secret).now()
        print(f'{service:<{left_column}} | {otp:{right_column}}')


if __name__ == '__main__':
    cli()
