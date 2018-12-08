import re, io
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name="easyTCP",
	version='0.5.3',
	url='https://github.com/dsal3389/easyTCP',
	download_url='https://github.com/dsal3389/easyTCP.git',
	license='Apache 2.0',
	author="Daniel Sonbolian",
	author_email='dsal3389@gmail.com',
	description="easy&fast way to create asyncronus server&clients",
	platform='any',
	python_requires='>=3.4.*',
	install_requires=[
		'cryptography==2.4.2'
	],
	packages=find_packages(),
	long_description=long_description,
	classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
	]
)
