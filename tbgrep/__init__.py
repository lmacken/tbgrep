#!/usr/bin/env python
# tbgrep - Python Traceback Extractor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011 Luke Macken <lmacken@redhat.com>

from collections import defaultdict
from operator import itemgetter

_file = open('/'.join(__file__.split('/')[:-1]) + '/README.rst')
__doc__ = _file.read()
_file.close()

tb_head = 'Traceback (most recent call last):'

class TracebackGrep(object):
    tb = index = None
    stats = firstline = prefix = False
    tracebacks = defaultdict(int)

    def __init__(self, stats=False):
        self.stats = stats

    def process(self, line):
        if self.tb:
            if line:
                line = line[self.index:]
                self.tb += line
                if line and line[0] != ' ':
                    tb = self.tb
                    self.tb = None
                    if self.stats:
                        self.tracebacks[tb] += 1
                    return tb
        elif tb_head in line:
            self.index = line.index(tb_head)
            self.tb = line[self.index:]

    def get_stats(self):
        return sorted(self.tracebacks.items(), key=itemgetter(1))

    def print_stats(self):
        header = lambda x: '== %s %s' % (x, '=' * (76 - len(x)))
        pluralize = lambda val, name: val == 1 and name or name + 's'
        stats = self.get_stats()
        for tb, num in stats:
            print header('%d %s' % (num, pluralize(num, 'occurence')))
            print
            print tb
        print '=' * 80
        num = len(stats)
        print "%d unique %s extracted" % (num, pluralize(num, 'traceback'))
