from kontur.checkgrammar.grammar import GrammarCheck, checkYaSpeller


class TestGetDictionary:
    def test_update_dict_from_file(self):
        check = GrammarCheck()
        check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
        assert len(check._dict) == 4, "Некорректно разобран словарь из файла"

    def test_update_two_dict_from_file(self):
        check = GrammarCheck()
        check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
        assert len(check._dict) == 4, "Некорректно разобран словарь из файла"

        check.update_dict_from_file("tests/fixture/dictionary/dict2.txt")
        assert len(check._dict) == 9, "Некорректно разобран словарь из файла"

    def test_update_two_dict_from_file_reverse(self):
        check = GrammarCheck()

        check.update_dict_from_file("tests/fixture/dictionary/dict2.txt")
        assert len(check._dict) == 5, "Некорректно разобран словарь из файла"

        check.update_dict_from_file("tests/fixture/dictionary/dict.txt")
        assert len(check._dict) == 9, "Некорректно разобран словарь из файла"

    def test_update_dict_from_bsl(self):
        check = GrammarCheck()
        check.update_dict_from_bsl("tests/fixture/dictionary/bsl-language-server.json")
        assert len(check._dict) == 5, "Некорректно разобран словарь из файла"


def test_add_src():
    check = GrammarCheck()
    check.add_src("tests/fixture/epf_mistakes/")
    assert len(check._src) == 1, "Не удалось добавить каталог исходников"

    check.add_src("tests/fixture/epf_right/")
    assert len(check._src) == 2, "Не удалось добавить каталог исходников"


class TestYaSpeller:
    def test_check_ya_speller_error(self):
        result = checkYaSpeller("Конртагент")
        assert result, "Не найдено ошибок"

    def test_check_ya_speller_no_error(self):
        result = checkYaSpeller("Контрагент")
        assert not result, "Найдены ошибки"

    def test_check_ya_speller_no_error_with_dict(self):
        result = checkYaSpeller("КоНрТаГеНт  ", tuple(["конртагент"]))

        assert not result, "Найдены ошибки"

    def test_check_ya_speller_no_error_if_in_suggest(self):
        result = checkYaSpeller("Картинка состояние отчета отправлен")
        assert not result, "Найдены ошибки"


class TestRunResult:
    def test_run(self, check_errors):

        assert check_errors._result
        assert "ОбработкаСОшибками.Форма" in check_errors._result

        elements = check_errors._result["ОбработкаСОшибками.Форма"]

        assert len(elements) == 5

    def test_has_error(self, check_errors):
        assert check_errors.has_errors

    def test_run_no_error(self, check_no_errors):
        assert not check_no_errors._result

    def test_has_no_error(self, check_no_errors):
        assert not check_no_errors.has_errors


class TestDumpResults:
    def test_dump_junit(self, check_errors, temp_xml):
        check_errors.dump_junit(temp_xml)
        must_be = [
            'failures="5"',
            "ГраппаСПолями.Заголовок",
            "Реквизит2.Заголовок",
        ]
        with open(temp_xml, "r", encoding="utf-8") as f:
            xml = f.read()
            for x in must_be:
                assert x in xml

    def test_dump_txt(self, check_errors, temp_txt):
        check_errors.dump_dict(temp_txt)
        with open(temp_txt, "r", encoding="utf-8") as f:
            output = [x.strip() for x in f.readlines()]

        assert "граппа" in output

    def test_print(self, check_errors, capsys):
        check_errors.print()
        captured = capsys.readouterr()
        must_be = [
            "ОбработкаСОшибками.Форма",
            "ГраппаСПолями.Заголовок",
            "Реквизит2.Заголовок",
        ]
        for x in must_be:
            assert x in captured.out

    def test_dump_junit_no_errors(self, check_no_errors, temp_xml):
        check_no_errors.dump_junit(temp_xml)
        with open(temp_xml, "r", encoding="utf-8") as f:
            xml = f.read()
            assert xml == '<?xml version="1.0" encoding="utf-8"?>\n<testsuites/>\n'

    def test_dump_txt_no_errors(self, check_no_errors, temp_txt):
        check_no_errors.dump_dict(temp_txt)
        with open(temp_txt, "r", encoding="utf-8") as f:
            output = [x.strip() for x in f.readlines()]

        assert not output

    def test_print_no_errors(self, check_no_errors, capsys):
        check_no_errors.print()
        captured = capsys.readouterr()
        assert "" in captured.out