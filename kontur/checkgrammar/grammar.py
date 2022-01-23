import json
import os

from junit_xml import TestCase, TestSuite
from pyaspeller import YandexSpeller
from wasabi import Printer

from kontur.checkgrammar import parse


class GrammarCheck:
    def __init__(self):

        self._src = []
        self._dict = []
        self._result = None

        self.__speller = YandexSpeller(lang="ru", ignore_urls=True, ignore_latin=True)

    def update_dict_from_file(self, path_to_dict: str):
        """
        Дополняет словарь исключений
                        :param path_to_dict: путь до файла со словарем
        """
        full_path = os.path.abspath(path_to_dict)
        assert os.path.exists(full_path), f"Не найден словарь {full_path}"

        with open(path_to_dict, "r", encoding="utf-8") as f:
            our_dict = [x.strip().lower() for x in f.readlines()]

        self._dict += our_dict

    def update_dict_from_bsl(self, bsl_settings="./.bsl-language-server.json"):
        """
        Дополняет словарь исключений из настроек bsl
                :param bsl_settings: путь до настроек .bsl-language-server.json
        """
        full_path = os.path.abspath(bsl_settings)
        assert os.path.exists(full_path), f"Не найдены настройки bsl language server {full_path}"

        with open(full_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        user_words_to_ignore = (
            data.get("diagnostics", {})
            .get("parameters", {})
            .get("Typo", {})
            .get("userWordsToIgnore", "")
        )
        assert (
            user_words_to_ignore
        ), "Не найден параметр diagnostics.parameters.Typo.userWordsToIgnore"

        our_dict = [x.strip().lower() for x in user_words_to_ignore.split(",")]

        self._dict += our_dict

    def add_src(self, src: str):
        """
        Добавить каталог с исходниками для обработки
                :param src: путь до каталога исходников
        """
        full_path = os.path.abspath(src)
        assert os.path.exists(full_path), f"Не найден каталог исходников {full_path}"

        self._src.append(full_path)

    def checkYaSpeller(self, text_for_check) -> list:
        result = []
        # find those words that may be misspelled
        check = self.__speller.spell(text_for_check)
        for res in check:
            if (
                res["s"] and res["word"].lower() not in self._dict
            ):  # Есть варианты замены
                result.append(f"{res['word']} -> {res['s']}")

        return result

    def run(self):

        assert self._src, "Не указаны каталоги для проверки"

        result = {}
        for src in self._src:
            objects = parse.parseSrc(src)

            for obj, elements in objects.items():

                for element, text in elements.items():
                    errors = self.checkYaSpeller(text)

                    if errors:
                        if obj not in result:
                            result[obj] = {}
                        result[obj].update({element: errors})

        self._result = result

    def dump_junit(self, path_to_xml):
        """
        Формирует отчет в формате JUnit
                :param path_to_xml: Путь до выгружаемого отчета
        """

        assert self._result is not None, "Проверка еще не была выполнена"

        full_path = os.path.abspath(path_to_xml)
        ts = []
        for obj, elements in self._result.items():

            test_cases = []
            for element, errors in elements.items():
                test_case = TestCase(element, classname=obj)
                test_case.add_error_info(
                    message="\n".join(errors),
                    error_type="Typo",
                )
                test_cases.append(test_case)

            ts.append(TestSuite(obj, test_cases))

        with open(full_path, "w", encoding="utf-8") as f:
            TestSuite.to_file(f, ts, prettyprint=False, encoding="utf-8")

    def print(self):
        assert self._result is not None, "Проверка еще не была выполнена"
        msg = Printer()
        for obj, elements in self._result.items():
            msg.divider(obj)
            for element, errors in elements.items():
                msg.warn(element)
                for error in errors:
                    msg.fail(error)

    @property
    def has_error(self):

        assert self._result is not None, "Проверка еще не была выполнена"

        return bool(self._result)
