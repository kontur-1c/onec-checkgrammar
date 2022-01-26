import os
import re
from setuptools import find_namespace_packages, setup

package_version = os.environ.get("VERSION", "0.0.0.dev0")

if not re.match(r"\d+\.\d+\.\d(\..*)?", package_version):
    package_version = "0.0.0-dev"
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

title = "onec-checkgrammar"
author = "a.krapivin"
email = "krapivin_andrey@mail.ru"
url = "https://github.com/kontur-1c/onec-grammarcheck"

requires = ["pyaspeller", "Click", "junit-xml", "wasabi", "tqdm"]
requires_test = ["pytest", "pytest-cov", "pytest-runner", "pytest-click"]
requires_dev = requires_test + ["black", "flake8"]

setup(
    name=title,
    version=package_version,
    description="Проверка орфографии элементов формы для 1с",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=requires,
    setup_requires=requires_dev,
    tests_require=requires_test,
    url=url,
    packages=find_namespace_packages(include=["kontur.*"]),
    entry_points={
        "console_scripts": ["onec-checkgrammar=kontur.checkgrammar.cli:cli"]
    },
    include_package_data=True,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
