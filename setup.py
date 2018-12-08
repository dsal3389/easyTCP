import re, io
from setuptools import setup, find_packages

setup(
	name="easyTCP",
	version='0.5.2',
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
	classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
	]
)
