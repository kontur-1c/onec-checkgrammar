import os
from xml.etree import ElementTree as ET

import pytest

from kontur.checkgrammar import parse

# region fixture


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


# endregion


class TestGetRUContent:
    def test_get_ru_content_none(self):
        result = parse.getRuContent(None)
        assert result is None, "None должен возвращать None"

    def test_get_ru_content_ru(self, ru_content):
        result = parse.getRuContent(ru_content)
        assert result == "Тест", "Должен получить секцию RU строки"

    def test_get_ru_content_no_ru(self, no_ru_content):
        result = parse.getRuContent(no_ru_content)
        assert result is None, "RU секции нет"


class TestParseElements:
    def test_none_child_items(self):
        result = parse.getChildItems(None)
        assert not result

    def test_no_child_items(self, empty):
        result = parse.getChildItems(empty)
        assert not result

    def test_child_items_title(self, button):

        result = parse.getChildItems(button)

        assert result

        assert "Тест.Заголовок" in result
        assert result["Тест.Заголовок"] == "Тестовая кнопка"

    def test_child_items_tooltip(self, button):

        result = parse.getChildItems(button)

        assert result

        assert "Тест.Подсказка" in result
        assert result["Тест.Подсказка"] == "Это тестовая подсказка"

    def test_child_items_extended_tooltip(self, button):

        result = parse.getChildItems(button)

        assert result

        assert "Тест.РасшПодсказка" in result
        assert result["Тест.РасшПодсказка"] == "Это тестовая расширенная подсказка"

    def test_skip_elements_without_title(self, page_no_title):
        result = parse.getChildItems(page_no_title)

        assert result

        check_list = [
            "ПолеБезЗаголовка.Заголовок",
            "ФлагБезЗаголовка.Заголовок",
            "ПереключательБезЗаголовка.Заголовок",
        ]

        for key in check_list:

            assert key not in result

    def test_skip_picture(self, picture):
        result = parse.getChildItems(picture)

        assert not result

    def test_parse_form_with_auto_commandbar(self):
        path = os.path.abspath(
            "tests/fixture/epf_mistakes/ОбработкаСОшибками/Forms/Форма/Ext/Form.xml"
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

    def test_parse_form_without_auto_commandbar(self):
        path = os.path.abspath(
            "tests/fixture/epf_mistakes/ОбработкаСОшибками/Forms/Тест_Форма/Ext/Form.xml"
        )
        result = parse.parseForm(path)

        assert result
        check_list = ["Реквизит1.Заголовок"]
        for key in check_list:
            assert key in result


class TestParseFolders:
    def test_parse_src(self):
        path = os.path.abspath("tests/fixture/epf_mistakes/")
        result = parse.parseSrc(path)

        assert result
        assert "ОбработкаСОшибками.Форма" in result

    def test_parse_and_exclude_src(self):
        path = os.path.abspath("tests/fixture/epf_mistakes/")
        result = parse.parseSrc(path, "[!Тест_*]*")

        assert result
        assert "ОбработкаСОшибками.Форма" in result
        assert "ОбработкаСОшибками.Тест_Форма" not in result
