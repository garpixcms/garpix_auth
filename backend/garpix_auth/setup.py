from setuptools import setup, find_packages
from os import path


here = path.join(path.abspath(path.dirname(__file__)), 'garpix_auth')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix-auth',
    version='2.1.0',
    description='',
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 1.11',
        'djangorestframework >= 3.8',
        'django-oauth-toolkit >= 1.1.2',
        'social-auth-app-django >= 2.1.0',
        'django-rest-framework-social-oauth2 >= 1.1.0',
    ],
)
