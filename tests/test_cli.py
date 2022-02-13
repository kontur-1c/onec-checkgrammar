import os

import pytest
from click.testing import CliRunner

from kontur.checkgrammar.cli import cli

# region fixtures


@pytest.fixture
def temp_xml(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("junit.xml")
    return fn


@pytest.fixture
def temp_txt(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("output.txt")
    return fn


# endregion


class TestSrcOption:
    def test_empty_src(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["-o", "output.txt"])

        assert result.exit_code == 1
        assert "Необходимо указать каталоги для проверки" in result.output

    def test_skip(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--skip", "Тест_*", "./tests/fixture/epf_mistakes/"]
        )

        assert result.exit_code == 1
        assert "Обнаружены ошибки" in result.output
        assert "ОбработкаСОшибками.Форма" in result.output
        assert "ОбработкаСОшибками.Тест_Форма" not in result.output

    def test_skip_short(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["-skip", "Тест_*", "./tests/fixture/epf_mistakes/"]
        )

        assert result.exit_code == 1
        assert "Обнаружены ошибки" in result.output
        assert "ОбработкаСОшибками.Форма" in result.output
        assert "ОбработкаСОшибками.Тест_Форма" not in result.output

    def test_multi_src(self):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["./tests/fixture/epf_mistakes/", "./tests/fixture/epf_right/"]
        )

        assert result.exit_code == 1
        assert "ОбработкаСОшибками.Форма" in result.output
        assert "ОбработкаБезОшибок.Форма" in result.output


class TestResultCheck:
    def test_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["./tests/fixture/epf_mistakes/"])

        assert result.exit_code == 1
        assert "Обнаружены ошибки" in result.output
        assert "ОбработкаСОшибками.Форма" in result.output

    def test_no_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["./tests/fixture/epf_right/"])

        assert result.exit_code == 0
        assert "Нет ошибок" in result.output


class TestWorkWithDictionary:
    def test_error_dict(self):
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

    def test_error_dict_short(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "-d",
                "./tests/fixture/dictionary/dict.txt",
                "./tests/fixture/epf_mistakes/",
            ],
        )

        assert result.exit_code == 1
        assert "палями" not in result.output

    def test_error_bsl(self):
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

    def test_error_bsl_short(self):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "-bsl",
                "./tests/fixture/dictionary/bsl-language-server.json",
                "./tests/fixture/epf_mistakes/",
            ],
        )

        assert result.exit_code == 1
        assert "палями" not in result.output


class TestOutputOption:
    def test_error_junit(self, temp_xml):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["--junit", temp_xml, "./tests/fixture/epf_mistakes/"]
        )

        assert result.exit_code == 1
        assert os.path.exists(temp_xml)

    def test_error_junit_short(self, temp_xml):
        runner = CliRunner()
        result = runner.invoke(cli, ["-j", temp_xml, "./tests/fixture/epf_mistakes/"])

        assert result.exit_code == 1
        assert os.path.exists(temp_xml)

    def test_output_dict(self, temp_txt):
        runner = CliRunner()
        result = runner.invoke(
            cli, ["./tests/fixture/epf_mistakes/", "--output", temp_txt]
        )

        assert result.exit_code == 1
        assert os.path.exists(temp_txt)

    def test_output_dict_short(self, temp_txt):
        runner = CliRunner()
        result = runner.invoke(cli, ["./tests/fixture/epf_mistakes/", "-o", temp_txt])

        assert result.exit_code == 1
        assert os.path.exists(temp_txt)
