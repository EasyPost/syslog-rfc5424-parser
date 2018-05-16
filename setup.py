from setuptools import setup, find_packages


setup(
    name="syslog-rfc5424-parser",
    version="0.1.4",
    author="James Brown",
    author_email="jbrown@easypost.com",
    url="https://github.com/easypost/syslog-rfc5424-parser",
    description="Parser for RFC5424-compatible Syslog messages",
    license="ISC",
    install_requires=[
        'pyparsing>=2.0,<3.0',
        'enum34'
    ],
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: ISC License (ISCL)",
    ]
)
