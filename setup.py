#!/usr/bin/env python

"""The setup script."""

import re
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pandas', 'numpy', 'plotly']

setup_requirements = ['pandas', 'numpy', 'plotly']

test_requirements = ['pandas', 'numpy', 'plotly']

VERSIONFILE = "viewclust/_version.py"
VERSTRLINE = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
MO = re.search(VSRE, VERSTRLINE, re.M)
if MO:
    VERSTR = MO.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    author="Tyler Collins",
    author_email='tk11br@sharcnet.ca',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package for visualizing cluster measures.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='viewclust',
    name='viewclust',
    packages=find_packages(include=['viewclust', 'viewclust.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Andesha/viewclust',
    version=VERSTR,
    zip_safe=False,
)
 