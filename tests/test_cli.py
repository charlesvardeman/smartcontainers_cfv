import pytest
from click.testing import CliRunner
from sc import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception


def test_cli_with_options(runner):
    # test option genMeta
    result = runner.invoke(cli.main, ['--genMeta=linux'])
    assert not result.exception
    assert result.exit_code == 0

    result = runner.invoke(cli.main,['--create="run /bin/bash"'])
    assert not result.exception
    assert result.exit_code == 0

