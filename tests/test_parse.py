import os
from xml.etree import ElementTree as ET

import pytest

from kontur.checkgrammar import parse


@pytest.fixture
def button():
    obj = ET.parse("tests/fixture/button.xml")
    return obj


@pytest.fixture
def page_no_title():
    obj = ET.parse("tests/fixture/noTitle.xml")
    return obj


@pytest.fixture
def picture():
    obj = ET.parse("tests/fixture/picture.xml")
    return obj


@pytest.fixture
def empty():
    obj = ET.parse("tests/fixture/empty.xml")
    return obj


@pytest.fixture
def ru_content():
    obj = ET.parse("tests/fixture/ruContent.xml")
    return obj


@pytest.fixture
def no_ru_content():
    obj = ET.parse("tests/fixture/noRuContent.xml")
    return obj


# region Тест получение RU контента


def test_get_ru_content_none():
    result = parse.getRuContent(None)
    assert result is None, "None должен возвращать None"


def test_get_ru_content_ru(ru_content):
    result = parse.getRuContent(ru_content)
    assert result == "Тест", "Должен получить секцию RU строки"


def test_get_ru_content_no_ru(no_ru_content):
    result = parse.getRuContent(no_ru_content)
    assert result is None, "RU секции нет"


# endregion

# region Тест разбора элементов формы


def test_none_child_items():
    result = parse.getChildItems(None)
    assert not result


def test_no_child_items(empty):
    result = parse.getChildItems(empty)
    assert not result


def test_child_items_title(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.Заголовок" in result
    assert result["Тест.Заголовок"] == "Тестовая кнопка"


def test_child_items_tooltip(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.Подсказка" in result
    assert result["Тест.Подсказка"] == "Это тестовая подсказка"


def test_child_items_extended_tooltip(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.РасшПодсказка" in result
    assert result["Тест.РасшПодсказка"] == "Это тестовая расширенная подсказка"


def test_skip_elements_without_title(page_no_title):
    result = parse.getChildItems(page_no_title)

    assert result

    check_list = [
        "ПолеБезЗаголовка.Заголовок",
        "ФлагБезЗаголовка.Заголовок",
        "ПереключательБезЗаголовка.Заголовок",
    ]

    for key in check_list:

        assert key not in result


def test_skip_picture(picture):
    result = parse.getChildItems(picture)

    assert not result


# endregion


# region Тест разбора больших объектов: обработок, конфигурации


def test_parse_form_with_auto_commandbar():
    path = os.path.abspath(
        "tests/fixture/epf_mistakes/ТестоваяОбработка/Forms/Форма/Ext/Form.xml"
    )
    result = parse.parseForm(path)

    assert result
    check_list = [
        "КнопкаКоманднойПанели.Заголовок",
        "ГруппаСДекорациями.Заголовок",
        "ГраппаСПолями.Заголовок",
        "ГруппаСКнопками.Заголовок",
        "Надпись.Заголовок",
        "Реквизит1.Заголовок",
        "Реквизит2.Заголовок",
        "Команда1.Заголовок",
        "Флаг.Заголовок",
        "Флаг.Подсказка",
        "Флаг.РасшПодсказка",
    ]
    for key in check_list:

        assert key in result


def test_parse_form_without_auto_commandbar():
    path = os.path.abspath(
        "tests/fixture/epf_right/ТестоваяОбработка/Forms/Форма/Ext/Form.xml"
    )
    result = parse.parseForm(path)

    assert result
    check_list = [
        "ГруппаСДекорациями.Заголовок",
        "ГраппаСПолями.Заголовок",
        "ГруппаСКнопками.Заголовок",
        "Надпись.Заголовок",
        "Реквизит1.Заголовок",
        "Реквизит2.Заголовок",
        "Команда1.Заголовок",
        "Флаг.Заголовок",
        "Флаг.Подсказка",
        "Флаг.РасшПодсказка",
    ]
    for key in check_list:

        assert key in result


def test_parse_src():
    path = os.path.abspath("tests/fixture/epf_mistakes/")
    result = parse.parseSrc(path)

    assert result
    assert "ТестоваяОбработка.Форма" in result


# endregion
