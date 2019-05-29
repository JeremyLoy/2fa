# 2fa
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

CLI for Time-Based OTP codes.

```shell
twofa add github $SECRETKEY
twofa copy github # copies OTP to clipboard
twofa # lists all registered services and their current OTP
twofa --json # same as above but in a machine readable format
twofa remove github # removes the service
```

## Local Development

Install [pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

```shell
pipenv sync --dev
```

This automatically configures a venv as well as installing twofa as an editable package.


## Installation outside of venv

TODO