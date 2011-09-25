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
