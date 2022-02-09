import glob
import os
from typing import Dict, Union
from xml.etree import ElementTree as Et

namespaces = {
    "logform": "http://v8.1c.ru/8.3/xcf/logform",
    "core": "http://v8.1c.ru/8.1/data/core",
    "xr": "http://v8.1c.ru/8.3/xcf/readable",
}


def getRuContent(obj: Et.Element) -> Union[str, None]:
    """
    Получает русское наименование элемента
        :param obj: Параметр элемента формы: Заголовок, Подсказка, Расширенная подсказка
        :return: Строку или None если не нашел
    """
    if obj is None:
        return None
    elements = obj.findall("core:item", namespaces)
    for element in elements:
        lang = element.find("core:lang", namespaces)
        if lang is not None and lang.text == "ru":
            content = element.find("core:content", namespaces)
            if content is not None:
                return content.text

    return None


def getChildItems(obj: Et.Element) -> Dict[str, str]:
    """
    Перебирает подчиненные элементы: кнопки, надписи, поля ввода и тд. Выделяет их заголовок, подсказку или
    расширенную подсказку. Рекурсивно вызывает обработку вложенных элементов.
    Например: Страница(Заголовок) - Командная панель - Кнопки(Заголовок, Подсказки)
        :param obj: Элемент формы
        :return: Словарь НазваниеЭлемента.Поле - Текст
    """
    result: Dict[str, str] = {}
    if obj is None:
        return result
    all_elements = obj.find("logform:ChildItems", namespaces)
    if all_elements is None:
        return result
    for element in all_elements:
        name = element.attrib.get("name")
        tag = element.tag[element.tag.find("}") + 1 :]
        title = element.find("logform:Title", namespaces)
        if title is not None:
            # Проверим виден ли заголовок
            title_location = element.find("logform:TitleLocation", namespaces)
            if (
                tag in ("InputField", "RadioButtonField", "CheckBoxField")
                and title_location is not None
                and title_location.text == "None"
            ):
                pass
            elif tag == "PictureDecoration":
                pass
            else:
                content = getRuContent(title)
                if content is not None:
                    result[f"{name}.Заголовок"] = content

        tooltip = element.find("logform:ToolTip", namespaces)
        if tooltip is not None:
            content = getRuContent(tooltip)
            if content is not None:
                result[f"{name}.Подсказка"] = content

        ext_tooltip = element.find("logform:ExtendedTooltip/logform:Title", namespaces)
        if ext_tooltip is not None:
            content = getRuContent(ext_tooltip)
            if content is not None:
                result[f"{name}.РасшПодсказка"] = content

        choice_list = element.findall("logform:ChoiceList/*", namespaces)
        if choice_list:
            num = 0
            for choice in choice_list:
                choice_value = choice.find("xr:Value", namespaces)
                if choice_value is None:
                    continue
                presentation = choice_value.find("logform:Presentation", namespaces)
                value = choice_value.find("logform:Value", namespaces)
                if presentation is not None and presentation.text is not None:
                    result[f"{name}.List{num}.Представление"] = presentation.text
                elif value is not None and value.text is not None:
                    result[f"{name}.List{num}.Значение"] = value.text
                num += 1

        result.update(getChildItems(element))
    return result


def parseForm(path_to_form: str) -> Dict[str, str]:
    """
    Разбор формы на элементы
            :param path_to_form: путь до файла формы
            :return: dict с элеметами формы и их текстами
    """
    form = Et.parse(path_to_form).getroot()

    bar = form.find("logform:AutoCommandBar", namespaces)
    buttons: Dict[str, str] = {}
    if bar is not None:
        buttons = getChildItems(bar)

    elements = getChildItems(form)

    return dict(elements, **buttons)


def parseSrc(path_to_src) -> Dict[str, Dict[str, str]]:
    """
    Разбор каталога исходников на формы и элементы
        :param path_to_src: путь до каталога исходников
        :return: dict с формами и элементами
    """
    full_path = os.path.abspath(path_to_src)
    files = glob.glob(f"{full_path}/**/Forms/*/Ext/Form.xml", recursive=True)
    result: Dict[str, Dict[str, str]] = {}
    for form_file in files:
        temp = form_file.split(os.path.sep)
        obj = temp[-5]
        form = temp[-3]
        result[f"{obj}.{form}"] = parseForm(form_file)

    return result
