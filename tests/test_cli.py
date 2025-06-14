import pytest
from typer.testing import CliRunner

from yt_quick_insights.cli import app

runner = CliRunner()


# TODO: Current Issue - Parameter.make_metavar() missing 1 required positional argument: 'ctx'
@pytest.mark.skip
def test_if_cli_help_command_works():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
