import os

import pytest
from click.testing import CliRunner

from kontur.checkgrammar.cli import cli


@pytest.fixture
def temp_xml(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("junit.xml")
    return fn


@pytest.fixture
def temp_txt(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("output.txt")
    return fn


def test_error():
    runner = CliRunner()
    result = runner.invoke(cli, ["./tests/fixture/epf_mistakes/"])

    assert result.exit_code == 1
    assert "Обнаружены ошибки" in result.output


def test_no_error():
    runner = CliRunner()
    result = runner.invoke(cli, ["./tests/fixture/epf_right/"])

    assert result.exit_code == 0
    assert "Нет ошибок" in result.output


def test_error_dict():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--dict",
            "./tests/fixture/dictionary/dict.txt",
            "./tests/fixture/epf_mistakes/",
        ],
    )

    assert result.exit_code == 1
    assert "палями" not in result.output


def test_error_bsl():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--bsl-settings",
            "./tests/fixture/dictionary/bsl-language-server.json",
            "./tests/fixture/epf_mistakes/",
        ],
    )

    assert result.exit_code == 1
    assert "палями" not in result.output


def test_error_junit(temp_xml):
    runner = CliRunner()
    result = runner.invoke(cli, ["--junit", temp_xml, "./tests/fixture/epf_mistakes/"])

    assert result.exit_code == 1
    assert os.path.exists(temp_xml)


def test_multi_src(temp_xml):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["./tests/fixture/epf_mistakes/", "./tests/fixture/epf_right/"]
    )

    assert result.exit_code == 1


def test_output_dict(temp_txt):
    runner = CliRunner()
    result = runner.invoke(cli, ["./tests/fixture/epf_mistakes/", "--output", temp_txt])

    assert result.exit_code == 1
    assert os.path.exists(temp_txt)
