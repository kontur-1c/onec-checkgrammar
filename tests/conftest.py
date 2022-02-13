from xml.etree import ElementTree as ET

import pytest

from kontur.checkgrammar.grammar import GrammarCheck


@pytest.fixture
def temp_xml(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("junit.xml")
    return fn


@pytest.fixture
def temp_txt(tmpdir_factory):
    fn = tmpdir_factory.mktemp("data").join("output.txt")
    return fn


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


@pytest.fixture(scope="class")
def check_errors():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
    check.add_src("tests/fixture/epf_mistakes/")

    check.run()

    return check


@pytest.fixture(scope="class")
def check_no_errors():
    check = GrammarCheck()
    check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
    check.add_src("tests/fixture/epf_right/")

    check.run()

    return check
