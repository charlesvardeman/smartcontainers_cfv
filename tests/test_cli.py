import pytest
from click.testing import CliRunner
from sc import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert not result.exception


def test_search(runner):
    # test option docker
    result = runner.invoke(cli.cli, input='search')
    assert not result.exception
    assert result.exit_code == 0

def test_config(runner):
    result = runner.invoke(cli.cli,input='config')
    assert not result.exception
    assert result.exit_code == 0

def test_docker(runner):
    result = runner.invoke(cli.cli,input='docker --help')
    assert not result.exception
    assert result.exit_code == 0
