# -*- python -*-

# pylogsparser - Logs parsers python library
#
# Copyright (C) 2011 Wallix Inc.
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
import unittest
from logsparser.lognormalizer import LogNormalizer
from lxml.etree import fromstring as XMLfromstring

class Test(unittest.TestCase):
    """Unit tests for logsparser.lognormalizer"""
    normalizer_path = os.environ['NORMALIZERS_PATH']
    
    def test_001_all_normalizers_activated(self):
        """ Verify that we have all normalizer
        activated when we instanciate LogNormalizer with
        an activate dict empty.
        """
        ln = LogNormalizer(self.normalizer_path)
        self.assertTrue(len(ln))
        self.assertEqual(len([an[0] for an in ln.get_active_normalizers() if an[1]]), len(ln))
        self.assertEqual(len(ln._cache), len(ln))

    def test_002_deactivate_normalizer(self):
        """ Verify that normalizer deactivation is working.
        """
        ln = LogNormalizer(self.normalizer_path)
        active_n = ln.get_active_normalizers()
        to_deactivate = active_n.keys()[:2]
        for to_d in to_deactivate:
            del active_n[to_d]
        ln.set_active_normalizers(active_n)
        ln.reload()
        self.assertEqual(len([an[0] for an in ln.get_active_normalizers() if an[1]]), len(ln))
        self.assertEqual(len(ln._cache), len(ln)-2)

    def test_003_activate_normalizer(self):
        """ Verify that normalizer activation is working.
        """
        ln = LogNormalizer(self.normalizer_path)
        active_n = ln.get_active_normalizers()
        to_deactivate = active_n.keys()[0]
        to_activate = to_deactivate
        del active_n[to_deactivate]
        ln.set_active_normalizers(active_n)
        ln.reload()
        # now deactivation should be done so reactivate
        active_n[to_activate] = True
        ln.set_active_normalizers(active_n)
        ln.reload()
        self.assertEqual(len([an[0] for an in ln.get_active_normalizers() if an[1]]), len(ln))
        self.assertEqual(len(ln._cache), len(ln))

    def test_004_normalizer_uuid(self):
        """ Verify that we get at least uuid tag
        """
        testlog = {'raw': 'a minimal log line'}
        ln = LogNormalizer(self.normalizer_path)
        ln.lognormalize(testlog)
        self.assertTrue('uuid' in testlog.keys())

    def test_005_normalizer_test_a_syslog_log(self):
        """ Verify that lognormalizer extracts
        syslog header as tags
        """
        testlog = {'raw': 'Jul 18 08:55:35 naruto app[3245]: body message'}
        ln = LogNormalizer(self.normalizer_path)
        ln.lognormalize(testlog)
        self.assertTrue('uuid' in testlog.keys())
        self.assertTrue('date' in testlog.keys())
        self.assertEqual(testlog['body'], 'body message')
        self.assertEqual(testlog['program'], 'app')
        self.assertEqual(testlog['pid'], '3245')

    def test_006_normalizer_test_a_syslog_log_with_syslog_deactivate(self):
        """ Verify that lognormalizer does not extract
        syslog header as tags when syslog normalizer is deactivated.
        """
        testlog = {'raw': 'Jul 18 08:55:35 naruto app[3245]: body message'}
        ln = LogNormalizer(self.normalizer_path)
        active_n = ln.get_active_normalizers()
        del active_n['syslog']
        ln.set_active_normalizers(active_n)
        ln.reload()
        ln.lognormalize(testlog)
        self.assertTrue('uuid' in testlog.keys())
        self.assertFalse('date' in testlog.keys())
        self.assertFalse('program' in testlog.keys())

    def test_004_normalizer_getsource(self):
        """ Verify we can retreive XML source
        of a normalizer.
        """
        ln = LogNormalizer(self.normalizer_path)
        source = ln.get_normalizer_source('syslog')
        self.assertEquals(XMLfromstring(source).getroottree().getroot().get('name'), 'syslog')

if __name__ == "__main__":
    unittest.main()
