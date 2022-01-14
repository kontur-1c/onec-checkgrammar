import os

from setuptools import find_namespace_packages, setup

package_version = os.environ.get("CI_COMMIT_TAG") or "0.dev0"

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

title = "kontur-retail1c-grammarnazi"
author = "1c_infra_dev"
email = "1c_infra_dev-aaaabcxg5jguh2uhywkaqukgp4@kontur.slack.com"
url = "https://git.skbkontur.ru/edi1c/grammarnazi"

requires = ["pyspeller=0.2.0"]
requires_dev = ["black", "pytest", "pytest-cov", "pytest-runner"]

setup(
    name=title,
    version=package_version,
    description="Проверка орфографии элементов формы",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=requires,
    setup_requires=requires_dev,
    tests_require=requires_dev,
    url=url,
    packages=find_namespace_packages(include=["kontur.*"]),
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
