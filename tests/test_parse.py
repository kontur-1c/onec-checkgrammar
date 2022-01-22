import os
from xml.etree import ElementTree as ET

import pytest

from kontur.checkgrammar import parse


@pytest.fixture
def button():
    data = """<?xml version="1.0"?>
        <ButtonGroup xmlns:v8="http://v8.1c.ru/8.1/data/core" xmlns="http://v8.1c.ru/8.3/xcf/logform" name="ГруппаТест" id="1249">
            <ChildItems>
                <Button name="Тест" id="65">
                    <Type>CommandBarButton</Type>
                    <CommandName>Form.Command.Тест</CommandName>
                    <Title>
                        <v8:item>
                            <v8:lang>ru</v8:lang>
                            <v8:content>Тестовая кнопка</v8:content>
                        </v8:item>
                    </Title>
                    <ToolTip>
                        <v8:item>
                            <v8:lang>ru</v8:lang>
                            <v8:content>Это тестовая подсказка</v8:content>
                        </v8:item>
                    </ToolTip>
                    <ExtendedTooltip name="ТестоваяПодсказка" id="1255">
                        <Title formatted="false">
                            <v8:item>
                                <v8:lang>ru</v8:lang>
                                <v8:content>Это тестовая расширенная подсказка</v8:content>
                            </v8:item>
                        </Title>
                    </ExtendedTooltip>
                </Button>
            </ChildItems>
        </ButtonGroup>
        """
    obj = ET.fromstring(data)
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


# endregion


def test_parseForm():
    path = os.path.abspath("fixture/epf/ТестоваяОбработка/Forms/Форма/Ext/Form.xml")
    result = parse.parseForm(path)

    assert result
    must_be = [
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
    for key in must_be:

        assert key in result


def test_parseSrc():
    path = os.path.abspath("fixture/epf/")
    result = parse.parseSrc(path)

    assert result
    assert "ТестоваяОбработка.Форма" in result
