from setuptools import setup

setup(
    name="logworks",
    packages=["logworks"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Logworks module",
    url="https://github.com/isilanes/logworks",
    author="Iñaki Silanes Cristóbal",
    author_email="isilanes@gmail.com",
    license="GPLv3",
    keywords = ["logging"],
    classifiers = [],
    zip_safe=False
)
