# -*- encoding: utf8 -*-
import os
from thumbnail_maker import __version__, __author__, __email__, __license__
from setuptools import setup, find_packages
from setuptools.command.test import test
from setuptools import setup


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests

        runtests()


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-thumbnail-maker',
    version=__version__,
    description='Thumbnail maker for Django',
    long_description=README,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    license=__license__,
    url='https://github.com/infinityxxx/django-thumbnail-maker',
    packages=find_packages(exclude=['tests', 'tests.*']),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
    ],
    install_requires=[
        'sorl-thumbnail',
    ],
    cmdclass={"test": TestCommand},
)
