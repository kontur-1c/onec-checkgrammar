[![Python tests](https://github.com/kontur-1c/onec-checkgrammar/actions/workflows/tests.yml/badge.svg)](https://github.com/kontur-1c/onec-checkgrammar/actions/workflows/tests.yml)
![PyPI - Downloads](https://img.shields.io:/pypi/dm/onec-checkgrammar)
[![codecov](https://codecov.io/gh/kontur-1c/onec-checkgrammar/branch/main/graph/badge.svg?token=GE7JETHL4C)](https://codecov.io/gh/kontur-1c/onec-checkgrammar)

# onec-checkgrammar

Проверка орфографии элементов форм

Можно проверять исходные файлы внешних обработок/отчетов и файлов конфигурации

## Установка

### Из пакетов

```bash
pip install onec-checkgrammar
```

### Из репозитория

```bash
pip install .
```

## Использование

### Простая проверка

```bash
onec-checkgrammar ./src
```

Будут выбраны все файлы форм в формате xml. Из них извлечены элементы для которых заданы:
* Заголовки
* Подсказки
* Расширенные подсказки

### Проверка нескольких папок

```bash
onec-checkgrammar ./src1 ./src2
```

### Результат проверки в формате JUnit 

```bash
onec-checkgrammar ./src --junit junit.xml
```

### Словари исключений

Для исключения терминов или каких-то других слов можно использовать словари

#### Явное указание

```bash
onec-checkgrammar ./src --dict dict.txt
```

Слова должны быть разделены переносом строк

Можно указать несколько словарей

```bash
onec-checkgrammar ./src --dict dict1.txt --dict dict2.txt
```

#### Настройки BSL language server

Если у Вас в настройках указаны исключения для опечаток, можно использовать их повторно

```bash
onec-checkgrammar ./src -bsl
```

Будут взяты настройки из файла *.bsl-language-server.json*

```bash
onec-checkgrammar ./src -bsl /my-bsl.json
```

Явное указание файла настроек



