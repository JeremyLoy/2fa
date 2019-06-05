import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pyperclip
from click.testing import CliRunner

import twofa


@patch("pyotp.totp.datetime")
@patch("twofa.FILE", Path(tempfile.mktemp()))
def test_all(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.utcfromtimestamp(0)

    service = "google.com"
    totp_epoch = "149389"

    runner = CliRunner()

    result = runner.invoke(twofa.add, [service], input="JBSWY3DPEHPK3PXP\n")
    assert result.exception is None
    assert 0 == result.exit_code

    result = runner.invoke(twofa.cli, ["--json"])
    assert result.exception is None
    assert 0 == result.exit_code
    assert totp_epoch == json.loads(result.stdout)[service]

    result = runner.invoke(twofa.copy, [service])
    assert result.exception is None
    assert 0 == result.exit_code
    assert totp_epoch == pyperclip.paste()

    result = runner.invoke(twofa.remove, [service])
    assert result.exception is None
    assert 0 == result.exit_code

    result = runner.invoke(twofa.cli, ["--json"])
    assert result.exception is None
    assert 0 == result.exit_code
    assert {} == json.loads(result.stdout)
