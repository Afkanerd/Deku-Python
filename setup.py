"""Setup Module"""

import os
from setuptools import find_packages, setup

f = open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8")
readme = f.read()
f.close()

setup(
    name="DekuPython",
    packages=find_packages(),
    version="0.1.0",
    description="Deku Python Library",
    long_description=readme,
    author="Afkanerd",
    author_email="info@afkanerd.com",
    license="The GNU General Public License v3.0",
    install_requires=["pika~=1.3.1", "phonenumbers~=8.13.7 "],
    test_suite="tests",
)
