from setuptools import setup, find_packages

setup(
    name='gotolong',
    version='0.0.1',
    utl='https://github.com/surinder432/gotolong',
    description='An investor stock advisor',
    author='Surinder Kumar',
    author_email='surinder.kumar.432@gmail.com',
    install_requires=['Django', 'prettytable'],
    packages=find_packages(),
    package_data={'': ['data/db/*.sql']},
)
