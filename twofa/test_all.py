import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pyperclip
from click.testing import CliRunner

import twofa


class AllTestCase(unittest.TestCase):
    @patch("pyotp.totp.datetime.datetime")
    @patch("twofa.FILE", Path(tempfile.mktemp()))
    def test_all(self, mock_datetime):
        setattr(mock_datetime, "now", lambda: datetime.utcfromtimestamp(0))

        service = "google.com"
        totp_epoch = "149389"

        runner = CliRunner()

        result = runner.invoke(twofa.add, [service], input="JBSWY3DPEHPK3PXP\n")
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)

        result = runner.invoke(twofa.cli, ["--json"])
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual("%s" % totp_epoch, json.loads(result.stdout)[service])

        result = runner.invoke(twofa.copy, [service])
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(totp_epoch, pyperclip.paste())

        result = runner.invoke(twofa.remove, [service])
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)

        result = runner.invoke(twofa.cli, ["--json"])
        self.assertFalse(result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertNotIn(service, json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
