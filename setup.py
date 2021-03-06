#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs

extra = {}
is_py3k = sys.version_info[0] == 3
if is_py3k:
    extra.update(use_2to3=True)

if sys.version_info < (2, 4):
    raise Exception('monblog requires Python 2.4 or higher.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # noqa

from distutils.command.install import INSTALL_SCHEMES

# -- Parse meta
import re
re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_vers = re.compile(r'VERSION\s*=\s*\((.*?)\)')
re_doc = re.compile(r'^"""(.+?)"""')
rq = lambda s: s.strip("\"'")


def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, rq(attr_value)), )


def add_version(m):
    v = list(map(rq, m.groups()[0].split(', ')))
    return (('VERSION', '.'.join(v[0:3]) + ''.join(v[3:])), )


def add_doc(m):
    return (('doc', m.groups()[0]), )

pats = {re_meta: add_default,
        re_vers: add_version,
        re_doc: add_doc}
here = os.path.abspath(os.path.dirname(__file__))
meta_fh = open(os.path.join(here, 'monblog/__init__.py'))
try:
    meta = {}
    for line in meta_fh:
        if line.strip() == '# -eof meta-':
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))
finally:
    meta_fh.close()
# --

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
src_dir = 'monblog'


def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = scheme['purelib']

for dirpath, dirnames, filenames in os.walk(src_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    for filename in filenames:
        if filename.endswith('.py'):
            packages.append('.'.join(fullsplit(dirpath)))
        else:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in
                filenames]])

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See http://pypi.python.org/pypi/monblog'

# -*- Installation Requires -*-
py_version = sys.version_info
is_jython = sys.platform.startswith('java')
is_pypy = hasattr(sys, 'pypy_version_info')


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(f):
    return filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), 'requirements', f)).readlines()])

install_requires = reqs('default.txt')

# -*- Tests Requires -*-

if is_py3k:
    tests_require = reqs('test-py3k.txt')
elif is_jython:
    tests_require = reqs('test-jython.txt')
elif is_pypy:
    tests_require = reqs('test-pypy.txt')
else:
    tests_require = reqs('test.txt')

if py_version[0:2] == (2, 5):
    tests_require.extend('test-py25.txt')

extra["entry_points"] = {
        "console_scripts" : [
            "monblog=monblog.bin:monblog"
            ]
        }

setup(
    name='monblog',
    version=meta['VERSION'],
    description=meta['doc'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    platforms=['any'],
    packages=packages,
    data_files=data_files,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Networking',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=long_description,
    **extra)
