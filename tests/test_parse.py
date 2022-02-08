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


# region Тест получение RU контента


def test_GetRuContentNone():
    result = parse.getRuContent(None)
    assert result is None, "None должен возвращать None"


def test_GetRuContentRu():
    data = """<?xml version="1.0"?>
    <Title xmlns:v8="http://v8.1c.ru/8.1/data/core">
        <v8:item>
            <v8:lang>ru</v8:lang>
            <v8:content>Тест</v8:content>
        </v8:item>
        <v8:item>
            <v8:lang>en</v8:lang>
            <v8:content>Test</v8:content>
        </v8:item>
    </Title>
    """
    obj = ET.fromstring(data)
    result = parse.getRuContent(obj)
    assert result == "Тест", "Должен получить секцию RU строки"


def test_GetRuContentNoRu():
    data = """<?xml version="1.0"?>
        <Title xmlns:v8="http://v8.1c.ru/8.1/data/core">
            <v8:item>
                <v8:lang>en</v8:lang>
                <v8:content>Test</v8:content>
            </v8:item>
        </Title>
        """
    obj = ET.fromstring(data)
    result = parse.getRuContent(obj)
    assert result is None, "RU секции нет"


# endregion

# region Тест разбора элементов формы


def test_NoChildItems():
    data = """<?xml version="1.0"?>
    <ButtonGroup xmlns:v8="http://v8.1c.ru/8.1/data/core" name="ГруппаКнопокЗагрузитьФичи" id="1249">
    </ButtonGroup>
    """
    obj = ET.fromstring(data)
    result = parse.getChildItems(obj)
    assert not result


def test_ChildItemsTitle(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.Заголовок" in result
    assert result["Тест.Заголовок"] == "Тестовая кнопка"


def test_ChildItemsTooltip(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.Подсказка" in result
    assert result["Тест.Подсказка"] == "Это тестовая подсказка"


def test_ChildItemsExtendedTooltip(button):

    result = parse.getChildItems(button)

    assert result

    assert "Тест.РасшПодсказка" in result
    assert result["Тест.РасшПодсказка"] == "Это тестовая расширенная подсказка"


def test_skipElementsWithoutTitle(page_no_title):
    result = parse.getChildItems(page_no_title)

    assert result

    check_list = [
        "ПолеБезЗаголовка.Заголовок",
        "ФлагБезЗаголовка.Заголовок",
        "ПереключательБезЗаголовка.Заголовок"]

    for key in check_list:

        assert key not in result

# endregion


def test_parseFormWithAutoCommandBar():
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
        "Картинка.Заголовок",
        "Реквизит1.Заголовок",
        "Реквизит2.Заголовок",
        "Команда1.Заголовок",
        "Флаг.Заголовок",
        "Флаг.Подсказка",
        "Флаг.РасшПодсказка",
    ]
    for key in check_list:

        assert key in result


def test_parseFormWithoutAutoCommandBar():
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
        "Картинка.Заголовок",
        "Реквизит1.Заголовок",
        "Реквизит2.Заголовок",
        "Команда1.Заголовок",
        "Флаг.Заголовок",
        "Флаг.Подсказка",
        "Флаг.РасшПодсказка",
    ]
    for key in check_list:

        assert key in result


def test_parseSrc():
    path = os.path.abspath("tests/fixture/epf_mistakes/")
    result = parse.parseSrc(path)

    assert result
    assert "ТестоваяОбработка.Форма" in result
