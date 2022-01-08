from click.testing import CliRunner

from unstar_pipfile.unstar_pipfile import unstar


def test_cli_without_pipfile():
    """Test running default command."""
    runner = CliRunner()
    result = runner.invoke(unstar)
    assert result.exit_code == 1
    assert "Can't find Pipfile" in result.output


def test_cli_without_pipfile():
    """Test displaying help message."""
    runner = CliRunner()
    result = runner.invoke(unstar, "--help")
    assert result.exit_code == 0
    assert "replace any stars" in result.output
