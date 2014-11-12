import sys
import types

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from nose.tools import eq_, assert_raises

from tbgrep import TracebackGrep

traceback = 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nException\n'

variations = [
"""
foo
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
Exception
bar
""",
"""
    foo
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    Exception
    bar
""",
"""
prefix    foo
prefix    Traceback (most recent call last):
prefix      File "<stdin>", line 1, in <module>
prefix    Exception
prefix    bar
""",
]

def get_input_file():
    input_file = StringIO()
    input_file.write("""
a
b
c
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
Exception
d
e
f
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
g
h
i
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'foo'
j
k
l
""".strip())
    input_file.seek(0)
    return input_file

input_lines = get_input_file().readlines()


def test_tbgrep():
    extractor = TracebackGrep()
    for variation in variations:
        found = False
        for line in variation.split('\n'):
            tb = extractor.process(line + '\n')
            if tb:
                found = True
                assert tb == traceback, repr(tb)
        assert found, "Couldn't extract traceback from: " + repr(variation)

def test_tbgrep_stats():
    extractor = TracebackGrep(stats=True)
    for variation in variations:
        for line in variation.split('\n'):
            extractor.process(line + '\n')
    stats = extractor.get_stats()
    assert len(stats) == 1, stats
    assert stats[0][1] == 3, stats[0][1]
    sys.stdout = StringIO()
    extractor.print_stats()
    assert '1 unique traceback extracted' in sys.stdout.getvalue()
    sys.stdout = sys.__stdout__

def test_command():
    from tbgrep.commands import main
    import sys
    orig_stdin = sys.stdin
    for variation in variations:
        stdin = StringIO()
#        stdin.write(variation)
        sys.stdin = stdin
        sys.argv = ['tbgrep', '--stats']
        main()
        assert '1 unique traceback extracted' in sys.stdout.getvalue(), sys.stdout
    sys.stdin = orig_stdin

def test_tracebacks_from_lines():
    from tbgrep import tracebacks_from_lines

    tracebacks = tracebacks_from_lines(get_input_file())

    eq_(type(tracebacks), types.GeneratorType)
    eq_(next(tracebacks), ''.join(input_lines[3:6]))
    eq_(next(tracebacks), ''.join(input_lines[9:12]))
    eq_(next(tracebacks), ''.join(input_lines[15:18]))

    assert_raises(StopIteration, next, tracebacks)


def test_tracebacks_from_file():
    from tbgrep import tracebacks_from_file

    tracebacks = tracebacks_from_file(get_input_file())

    eq_(type(tracebacks), types.GeneratorType)
    eq_(next(tracebacks), ''.join(input_lines[3:6]))
    eq_(next(tracebacks), ''.join(input_lines[9:12]))
    eq_(next(tracebacks), ''.join(input_lines[15:18]))

    assert_raises(StopIteration, next, tracebacks)


def test_tracebacks_from_file_reverse():
    from tbgrep import tracebacks_from_file

    tracebacks = tracebacks_from_file(get_input_file(), reverse=True)
    eq_(next(tracebacks), ''.join(input_lines[15:18]))
    eq_(next(tracebacks), ''.join(input_lines[9:12]))
    eq_(next(tracebacks), ''.join(input_lines[3:6]))

    assert_raises(StopIteration, next, tracebacks)


def test_last_traceback_from_file():
    from tbgrep import last_traceback_from_file

    traceback = last_traceback_from_file(get_input_file())
    eq_(traceback, ''.join(input_lines[15:18]))
