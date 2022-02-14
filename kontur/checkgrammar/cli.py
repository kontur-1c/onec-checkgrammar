import sys

import click

from kontur.checkgrammar.grammar import GrammarCheck


@click.command()
@click.argument("src", envvar="SRC", nargs=-1)
@click.option(
    "--dict",
    "-d",
    "dictionary",
    default=None,
    multiple=True,
    help="Словари исключений из проверки",
)
@click.option(
    "--bsl-settings",
    "-bsl",
    "bsl",
    is_flag=False,
    flag_value=".bsl-language-server.json",
    help="Получить словарь из настроек bsl-language-server.json",
)
@click.option("--dry-run", "dry_run", is_flag=True, help="Не ронять тесты")
@click.option(
    "--junit", "-j", "junit", default=None, help="Файл отчета в формате junit"
)
@click.option("--output", "-o", "output", default=None, help="Файл для ошибок")
@click.option(
    "--skip",
    "-skip",
    "skip_pattern",
    default=None,
    help="Паттерн имени файла(glob), чтобы пропускать формы",
)
def cli(src, skip_pattern, dictionary, bsl, junit, output, dry_run):
    """Проверка орфографии элементов форм в каталоге SRC.

    SRC каталог исходников конфигурации или внешней обработки/отчета.

    Можно указать несколько через пробел"""

    if not src:
        print("Необходимо указать каталоги для проверки", file=sys.stderr)
        sys.exit(1)

    check = GrammarCheck()
    for d in dictionary:
        check.update_dict_from_file(d)

    if bsl:
        check.update_dict_from_bsl(bsl)

    if skip_pattern:
        check.add_skip_pattern(skip_pattern)

    for s in src:
        check.add_src(s)

    check.run()

    if junit is not None:
        check.dump_junit(junit)

    if output is not None:
        check.dump_dict(output)

    if check.has_errors:
        print("Обнаружены ошибки", file=sys.stderr)
        check.print()
        if not dry_run:
            sys.exit(1)
    else:
        print("Нет ошибок", file=sys.stdout)
        sys.exit(0)


if __name__ == "__main__":
    cli(sys.argv[1:])
