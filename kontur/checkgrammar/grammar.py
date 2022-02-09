import json
import os
import re
from datetime import datetime
from functools import lru_cache
from typing import List

import junit_xml
from pyaspeller import YandexSpeller
from tqdm import tqdm
from wasabi import Printer

from kontur.checkgrammar import parse

ya_speller = YandexSpeller(lang="ru", ignore_urls=True, ignore_latin=True)


class Error:
    def __init__(self, form: str, element: str, text: str, errors: List[str]):
        self.form = form
        self.element = element
        self.text = text
        self.errors = errors


class GrammarError:
    def __init__(self, word: str, variants: List[str]):
        self.word = word
        self.variants = variants

    def __str__(self):
        return f"{self.word} -> {self.variants}"


@lru_cache(maxsize=2048)
def checkYaSpeller(text: str, out_dict=tuple()) -> List[GrammarError]:
    # Подготовить текст. Спеллер плохо проверяет слова с цифрами
    result = []

    check = ya_speller.spell(text)
    for res in check:
        if (
            res["s"]
            and res["word"].lower() not in out_dict
            and res["word"].lower() not in res["s"]
        ):  # Есть варианты замены
            result.append(GrammarError(res["word"], res["s"]))

    return result


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

        start_time = datetime.now()
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

                    text_to_check = " ".join(
                        [re.sub(r"[0-9]+", "", x) for x in text.split(" ")]
                    )

                    errors = checkYaSpeller(text_to_check, our_dict)

                    if errors:
                        if obj not in result:
                            result[key] = []
                        result[key].append(Error(obj, element, text, errors))
        msg = Printer()
        msg.divider("СТАТИСТИКА", char="*")
        msg.info(f"Время {datetime.now() - start_time}")
        msg.info(f"Обнаружено ошибок {sum([len(x) for x in result.items()])}")
        msg.info(f"{checkYaSpeller.cache_info()}")
        msg.divider("=", char="*")

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

    def dump_dict(self, path):
        """
        Выгрузка отчета в файл. Чтобы было проще готовить файл исключений
        :param path: путь для выгрузки отчета
        """
        full_path = os.path.abspath(path)
        result = set()
        for obj, details in self._result.items():
            for data in details:
                for error in data.errors:
                    result.add(error.word.lower())

        with open(full_path, "w", encoding="utf-8") as f:
            for s in result:
                f.write(s + "\n")

    @property
    def has_errors(self) -> bool:
        """
        Были ошибки при проверке
            :return: bool
        """
        assert self._result is not None, "Проверка еще не была выполнена"

        return bool(self._result)
