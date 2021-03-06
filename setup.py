# Standard libs:
from setuptools import setup, find_packages


# Functions:
def long_description():
    with open("README.md", "r") as f:
        return f.read()

# Meat:
setup(
    name="logworks",
    packages=["logworks"],
    package_dir={"logworks": "src"},  # directory "src" contains package "logworks"
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="logworks is a convenience wrapper for the logging Python module.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/isilanes/logworks",
    author="Iñaki Silanes Cristóbal",
    author_email="isilanes@gmail.com",
    keywords=["logging"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
