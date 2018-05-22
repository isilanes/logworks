from setuptools import setup


def long_description():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="logworks",
    packages=["logworks"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="logworks is a convenience wrapper for the logging Python module.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/isilanes/logworks",
    author="Iñaki Silanes Cristóbal",
    author_email="isilanes@gmail.com",
    license="GPLv3",
    keywords=["logging"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ),
    zip_safe=False
)
