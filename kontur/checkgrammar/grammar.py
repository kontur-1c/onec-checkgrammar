import json
import os
from functools import lru_cache
from typing import List

import junit_xml
from pyaspeller import YandexSpeller
from tqdm import tqdm
from wasabi import Printer

from kontur.checkgrammar import parse

ya_speller = YandexSpeller(lang="ru", ignore_urls=True, ignore_latin=True)


@lru_cache(maxsize=2048)
def checkYaSpeller(text: str, out_dict=tuple()) -> List[str]:
    result = []
    # find those words that may be misspelled
    check = ya_speller.spell(text)
    for res in check:
        if res["s"] and res["word"].lower() not in out_dict:  # Есть варианты замены
            result.append(f"{res['word']} -> {res['s']}")

    return result


class Error:
    def __init__(self, form: str, element: str, text: str, errors: List[str]):
        self.form = form
        self.element = element
        self.text = text
        self.errors = errors


class GrammarCheck:
    def __init__(self):

        self._src = []
        self._dict = []
        self._result = None

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
        assert os.path.exists(
            full_path
        ), f"Не найдены настройки bsl language server {full_path}"

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

        self._src.append(src)

    def run(self):
        """
        Запуск проверки орфографии
        """
        assert self._src, "Не указаны каталоги для проверки"

        result = {}
        our_dict = tuple(self._dict)
        for src in self._src:
            objects = parse.parseSrc(src)

            for obj, elements in objects.items():
                if len(self._src) == 1:
                    key = obj
                else:
                    key = f"{src}->{obj}"
                for element, text in tqdm(elements.items(), desc=obj):
                    if len(text) <= 3:
                        continue

                    errors = checkYaSpeller(text, our_dict)

                    if errors:
                        if obj not in result:
                            result[key] = []
                        result[key].append(Error(obj, element, text, errors))
        print(checkYaSpeller.cache_info())
        self._result = result

    def dump_junit(self, path_to_xml):
        """
        Формирует отчет в формате JUnit
                :param path_to_xml: Путь до выгружаемого отчета
        """

        assert self._result is not None, "Проверка еще не была выполнена"

        full_path = os.path.abspath(path_to_xml)
        ts = []
        for obj, details in self._result.items():

            test_cases = []
            for data in details:
                test_case = junit_xml.TestCase(
                    data.element,
                    classname=obj,
                    allow_multiple_subelements=True,
                    stderr=f"Возможно опечатка в тексте: {data.text}",
                )

                for error in data.errors:
                    test_case.add_failure_info(error, failure_type="WARNING")
                test_cases.append(test_case)

            ts.append(junit_xml.TestSuite(obj, test_cases))

        with open(full_path, "w", encoding="utf-8") as f:
            junit_xml.to_xml_report_file(f, ts, encoding="utf-8")

    def print(self):
        """
        Вывод на экран результатов проверки
        """
        assert self._result is not None, "Проверка еще не была выполнена"
        msg = Printer()
        for obj, details in self._result.items():
            msg.divider(obj)
            for data in details:
                msg.warn(data.element)
                for error in data.errors:
                    msg.fail(error)

    @property
    def has_errors(self) -> bool:
        """
        Признак что были ошибки при проверке
        :return:
        """
        assert self._result is not None, "Проверка еще не была выполнена"

        return bool(self._result)
