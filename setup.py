import os
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dali",
    version = "0.9",
    author = "John Shimek",
    author_email = "varikin@gmail.com",
    description = ("The website of jesleephotos.com, Something Amazing!"),
    license = "Apache Software License 2.0",
    keywords = "django gallery",
    url = "http://github.com/varikin/dali",
    packages = ['dali'],
    long_description = read('README'),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Artistic Software",
        "Framework :: Django",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_ok = False,
) 
