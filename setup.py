# -*- python -*-

# pylogsparser - Logs parsers python library
#
# Copyright (C) 2011 Wallix SARL
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import os
import glob
from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

data = glob.glob('normalizers/*.xml')
data.extend(glob.glob('normalizers/*.template'))
data.extend(glob.glob('normalizers/*.dtd'))

setup(
    name = "pylogsparser",
    version = "0.1",
    author = "Wallix",
    author_email = "opensource@wallix.org",
    description = ("A log parser library packaged with a set of ready to use parsers (DHCPd, Squid, Apache, ...)"),
    license = "LGPL",
    keywords = "log parser xml library python",
    url = "http://www.wallix.org/pylogsparser-project/",
    packages=['logsparser', 'tests'],
    data_files=[('share/normalizers', data)],
    requires=['lxml', 'pytz'],
    long_description=read('README.rst'),
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
)
