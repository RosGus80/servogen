import os
from setuptools import setup, find_packages

setup(
    name='servogen',
    version='0.0.1',
    packages=find_packages(where='src'),
    install_requires=[
        'Jinja2==3.1.6',
        'setuptools==65.5.0',
        'appdirs==1.4.4',
    ],
    entry_points={'console_scripts': ['servogen=servogen.main:main']},
    package_dir={'': 'src'},
    package_data={
        'servogen': ['templates/*.html', 'templates/*.css', 'css/*.css']
    },
    include_package_data=True,
)
