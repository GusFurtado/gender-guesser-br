from setuptools import setup
from os import path


def get_long_description() -> str:
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as file:
        return file.read()


def get_version() -> str:
    with open("gender_guesser_br/__init__.py", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("__version__"):
                return line.split('"')[1]
        raise RuntimeError("Versão não encontrada.")


setup(
    name="gender_guesser_br",
    packages=["gender_guesser_br"],
    version=get_version(),
    license="MIT",
    python_requires=">=3.6",
    description="Versão brasileira do pacote Python para adivinhar o gênero de um nome próprio.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Gustavo Furtado",
    author_email="gustavofurtado2@gmail.com",
    url="https://github.com/GusFurtado/gender_guesser_br",
    download_url=f"https://github.com/GusFurtado/gender_guesser_br/archive/{get_version()}.tar.gz",
    keywords=["brasil", "ibge", "dadosabertos", "gender", "genero"],
    install_requires=["DadosAbertosBrasil>=1.0.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Portuguese (Brazilian)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
