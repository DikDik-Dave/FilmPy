from setuptools import setup, find_packages
setup(
    name='FilmPy',
    version='25.2.0.rc0',
    packages=find_packages(include=['FilmPy', 'FilmPy.*']),
    package_data = {"FilmPy.assets": ["**/*"]}
)