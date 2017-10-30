from setuptools import setup

setup(
    name="logworks",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Logworks module",
    url="https://github.com/isilanes/logworks",
    author="Iñaki Silanes Cristóbal",
    author_email="isilanes@gmail.com",
    license="GPLv3",
    packages=["logworks"],
    zip_safe=False
)
