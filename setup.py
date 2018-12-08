import re, io
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name="easyTCP",
	version='0.6.0',
	url='https://github.com/dsal3389/easyTCP',
	download_url='https://github.com/dsal3389/easyTCP.git',
	license='IMT',
	author="Daniel Sonbolian",
	author_email='dsal3389@gmail.com',
	description="easy&fast way to create asyncronus server&clients",
	python_requires='>=3.4.*',
	install_requires=[
		'cryptography==2.4.2'
	],
	packages=[
                'easyTCP',
                'easyTCP.CLIENT',
                'easyTCP.CLIENT.backend',
                'easyTCP.CLIENT.utils',
                'easyTCP.SERVER',
                'easyTCP.SERVER.backend',
                'easyTCP.SERVER.utils'
            ],
	long_description=long_description,
	classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
	]
)
