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

import sys
import fileinput

import tbgrep

__doc__ = tbgrep.__doc__

def main():
    stats = False
    if '--stats' in sys.argv:
        stats = True
        sys.argv.remove('--stats')

    extractor = tbgrep.TracebackGrep(stats=stats)

    for line in fileinput.input():
        tb = extractor.process(line)
        if not stats and tb:
            print tb
    if stats:
        extractor.print_stats()

if __name__ == '__main__':
    main()
