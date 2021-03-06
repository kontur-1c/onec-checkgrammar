import kontur.pie as pie


# Путь до рантайма платформы
if pie.os.name == "posix":
    pie.v83_bin = "/opt/1C/v8.3/x86_64"
else:
    pie.v83_bin = "C:\\Program Files (x86)\\1cv8\\8.3.16.1063\\bin"


def dump():
    with pie.ib.TempIB():
        pie.dump_epf(
            epf="tests/fixture/epf_mistakes/ОбработкаСОшибками.epf",
            epf_xml="tests/fixture/epf_mistakes/ОбработкаСОшибками.xml",
        )

        pie.dump_epf(
            epf="tests/fixture/epf_right/ОбработкаБезОшибок.epf",
            epf_xml="tests/fixture/epf_right/ОбработкаБезОшибок.xml",
        )


def build():
    with pie.ib.TempIB():
        pie.build_epf(
            "tests/fixture/epf_mistakes/ОбработкаСОшибками.epf",
            "tests/fixture/epf_mistakes/ОбработкаСОшибками.xml",
        )

        pie.build_epf(
            "tests/fixture/epf_right/ОбработкаБезОшибок.epf",
            "tests/fixture/epf_right/ОбработкаБезОшибок.xml",
        )
