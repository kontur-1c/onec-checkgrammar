# onec-grammarcheck

Проверка орфографии элементов форм

Можно проверять исходные файлы внешних обработок/отчетов и файлов конфигурации

## Установка

### Из пакетов (coming soon)

```bash
pip install onec-grammarcheck
```

### Из репозитория

```bash
pip install .
```

## Использование

### Простая проверка

```bash
onec-grammarcheck ./src
```

Будут выбраны все файлы форм в формате xml. Из них извлечены элементы для которых заданы:
* Заголовки
* Подсказки
* Расширенные подсказки

### Проверка нескольких папок

```bash
onec-grammarcheck ./src1 ./src2
```

### Результат проверки в формате JUnit 

```bash
onec-grammarcheck ./src --junit junit.xml
```

### Словари исключений

Для исключения терминов или каких-то других слов можно использовать словари

#### Явное указание

```bash
onec-grammarcheck ./src --dict dict.txt
```

Слова должны быть разделены переносом строк

Можно указать несколько словарей

```bash
onec-grammarcheck ./src --dict dict1.txt --dict dict2.txt
```

#### Настройки BSL language server

Если у Вас в настройках указаны исключения для опечаток, можно использовать их повторно

```bash
onec-grammarcheck ./src -bsl
```

Будут взяты настройки из файла *.bsl-language-server.json*

```bash
onec-grammarcheck ./src -bsl /my-bsl.json
```

Явное указание файла настроек



