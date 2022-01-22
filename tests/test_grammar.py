import pytest

from kontur.checkgrammar.grammar import GrammarCheck


@pytest.fixture(scope="session")
def temp_xml(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("junit.xml")
    return fn


@pytest.fixture
def check():
    check = GrammarCheck()
    check.update_dict_from_file("fixture/dictionary/dict.txt")
    check.add_src("fixture/epf/")

    check.run()

    return check


def test_update_dict_from_file():
    check = GrammarCheck()
    check.update_dict_from_file("fixture/dictionary/dict.txt")

    assert len(check._dict) == 3, "Некорректно разобран словарь из файла"


def test_update_dict_from_bsl():
    check = GrammarCheck()
    check.update_dict_from_bsl("fixture/dictionary/bsl-language-server.json")

    assert len(check._dict) == 4, "Некорректно разобран словарь из файла"


def test_add_src():
    check = GrammarCheck()
    check.add_src("fixture/epf/")

    assert len(check._src) == 1, "Не удалось добавить каталог исходников"


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
    check.update_dict_from_file("fixture/dictionary/dict.txt")
    result = check.checkYaSpeller("КоНрТаГеНт  ")

    assert not result, "Найдены ошибки"


def test_run(check):

    assert check._result
    assert "ТестоваяОбработка.Форма" in check._result

    elements = check._result["ТестоваяОбработка.Форма"]

    assert len(elements) == 3


def test_dump_junit(check, temp_xml):
    check.dump_junit(temp_xml)
    must_be = [
        'errors="3"',
        "ГраппаСПолями.Заголовок",
        "ГраппаСПолями.Подсказка",
        "Реквизит2.Заголовок",
    ]
    with open(temp_xml, "r", encoding="utf-8") as f:
        xml = f.read()
        for x in must_be:
            assert x in xml


def test_print(check, capsys):
    check.print()
    captured = capsys.readouterr()
    must_be = [
        "ТестоваяОбработка.Форма",
        "ГраппаСПолями.Заголовок",
        "ГраппаСПолями.Подсказка",
        "Реквизит2.Заголовок",
    ]
    for x in must_be:
        assert x in captured.out
