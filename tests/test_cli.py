from typer.testing import CliRunner

from yt_quick_insights.cli import app

runner = CliRunner()


def test_if_cli_help_command_works():
    result = runner.invoke(app, ["download", "--help"])
    assert result.exit_code == 0
