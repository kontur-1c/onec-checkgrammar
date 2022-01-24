import pytest

from kontur.checkgrammar.grammar import GrammarCheck


@pytest.fixture
def temp_xml(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("junit.xml")
    return fn


@pytest.fixture
def check_errors():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
    check.add_src("tests/fixture/epf_mistakes/")

    check.run()

    return check


@pytest.fixture
def check_no_errors():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
    check.add_src("tests/fixture/epf_right/")

    check.run()

    return check


def test_update_dict_from_file():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")

    assert len(check._dict) == 4, "Некорректно разобран словарь из файла"


def test_update_dict_from_bsl():
    check = GrammarCheck()
    check.update_dict_from_bsl("tests/fixture/dictionary/bsl-language-server.json")

    assert len(check._dict) == 5, "Некорректно разобран словарь из файла"


def test_add_src():
    check = GrammarCheck()
    check.add_src("tests/fixture/epf_mistakes/")

    assert len(check._src) == 1, "Не удалось добавить каталог исходников"

    check.add_src("tests/fixture/epf_right/")
    assert len(check._src) == 2, "Не удалось добавить каталог исходников"


def test_check_ya_speller_error():
    check = GrammarCheck()
    result = check.checkYaSpeller("Конртагент")

    assert result, "Не найдено ошибок"


def test_check_ya_speller_no_error():
    check = GrammarCheck()
    result = check.checkYaSpeller("Контрагент")

    assert not result, "Найдены ошибки"


def test_check_ya_speller_no_error_with_dict():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
    result = check.checkYaSpeller("КоНрТаГеНт  ")

    assert not result, "Найдены ошибки"


# region Run with errors


def test_run(check_errors):
    assert check_errors._result
    assert "ТестоваяОбработка.Форма" in check_errors._result

    elements = check_errors._result["ТестоваяОбработка.Форма"]

    assert len(elements) == 3


def test_has_error(check_errors):
    assert check_errors.has_errors


def test_dump_junit(check_errors, temp_xml):
    check_errors.dump_junit(temp_xml)
    must_be = [
        'failures="3"',
        "ГраппаСПолями.Заголовок",
        "Реквизит2.Заголовок",
    ]
    with open(temp_xml, "r", encoding="utf-8") as f:
        xml = f.read()
        for x in must_be:
            assert x in xml


def test_print(check_errors, capsys):
    check_errors.print()
    captured = capsys.readouterr()
    must_be = [
        "ТестоваяОбработка.Форма",
        "ГраппаСПолями.Заголовок",
        "Реквизит2.Заголовок",
    ]
    for x in must_be:
        assert x in captured.out


# endregion

# region Run without errors


def test_run_no_error(check_no_errors):
    assert not check_no_errors._result


def test_has_no_error(check_no_errors):
    assert not check_no_errors.has_errors


def test_dump_junit_no_error(check_no_errors, temp_xml):
    check_no_errors.dump_junit(temp_xml)
    with open(temp_xml, "r", encoding="utf-8") as f:
        xml = f.read()
        assert xml == '<?xml version="1.0" encoding="utf-8"?>\n<testsuites/>\n'


def test_print_no_error(check_no_errors, capsys):
    check_no_errors.print()
    captured = capsys.readouterr()
    assert "" in captured.out


# endregion
