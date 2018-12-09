import re
import os
from setuptools import setup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'easyTCP', '__init__.py'), 'r')as f:
	version = re.search("__version__ = '(.*?)'", f.read()).group(1)

with open("README.md", "r") as f:
    long_description = f.read()


setup(
	name="easyTCP",
	version=version,
	url='https://github.com/dsal3389/easyTCP',
	download_url='https://github.com/dsal3389/easyTCP.git',
	license='IMT',
	author="Daniel Sonbolian",
	author_email='dsal3389@gmail.com',
	description="easy&fast way to create asyncronus server&clients",
	python_requires='>=3.5.*',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
	]
)
