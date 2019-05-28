# 2fa

CLI for Time-Based OTP codes.

```shell
twofa add github $SECRETKEY
twofa copy github # copies OTP to clipboard
twofa # lists all registered services and their current OTP
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