import click
from kontur.checkgrammar.grammar import GrammarCheck
import sys


@click.command()
@click.argument("src", envvar="SRC", nargs=-1)
@click.option(
    "-d",
    "--dict",
    "dictionary",
    default=None,
    multiple=True,
    help="Словари исключений из проверки",
)
@click.option(
    "-bsl",
    "--bsl-settings",
    "bsl",
    is_flag=False,
    flag_value="bsl-language-server.json",
    help="Получить словарь из настроек bsl-language-server.json",
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help="Не ронять тесты"

)
@click.option("--junit", default=None, help="Файл отчета в формате junit")
def cli(src, dictionary, bsl, junit, dry_run):
    """Проверка орфографии элементов форм в каталоге SRC.

    SRC каталог исходников конфигурации или внешней обработки/отчета.

    Можно указать несколько через пробел"""

    check = GrammarCheck()
    for d in dictionary:
        check.update_dict_from_file(d)

    if bsl:
        check.update_dict_from_bsl(bsl)

    for s in src:
        check.add_src(s)

    check.run()

    if junit is not None:
        check.dump_junit(junit)

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