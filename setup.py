import sys

from setuptools import setup, find_packages


def install_requires():
    if sys.version_info >= (3, 4):
        return ['lark-parser==0.6.*']
    else:
        return ['lark-parser==0.6.*', 'enum34']

setup(
    name="syslog-rfc5424-parser",
    version="0.3.2",
    author="James Brown",
    author_email="jbrown@easypost.com",
    url="https://github.com/easypost/syslog-rfc5424-parser",
    description="Parser for RFC5424-compatible Syslog messages",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license="ISC",
    install_requires=install_requires(),
    project_urls={
        'Issue Tracker': 'https://github.com/easypost/syslog-rfc5424-parser/issues',
        'Documentations': 'https://syslog-rfc5424-parser.readthedocs.io/en/latest/',
    },
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: ISC License (ISCL)",
    ]
)
