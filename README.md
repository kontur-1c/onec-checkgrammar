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

### Исключение форм из проверки

```bash
onec-checkgrammar --skip Тест_* ./src1 
```

Исключит все формы начинающиеся с префикса "Тест_". Подробнее: документация glob

### Результат проверки в формате JUnit 

```bash
onec-checkgrammar --junit junit.xml ./src
```

### Результат проверки в отдельный файл

```bash
onec-checkgrammar --output temp.txt ./src
```

В файл будут добавлены все слова с ошибками. Удобно подготовить файл словаря исключений

### Словари исключений

Для исключения терминов или каких-то других слов можно использовать словари

#### Явное указание

```bash
onec-checkgrammar --dict dict.txt ./src
```

Слова должны быть разделены переносом строк

Можно указать несколько словарей

```bash
onec-checkgrammar --dict dict1.txt --dict dict2.txt ./src
```

#### Настройки BSL language server

Если у Вас в настройках указаны исключения для опечаток, можно использовать их повторно

```bash
onec-checkgrammar --bsl-settings --dict dict1.txt ./src
```

Будут взяты настройки из файла *.bsl-language-server.json*

```bash
onec-checkgrammar -bsl /my-bsl.json ./src
```

Явное указание файла настроек
