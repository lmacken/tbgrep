Traceback Grep
==============

.. image:: https://api.travis-ci.org/lmacken/tbgrep.png?branch=master
   :target: http://travis-ci.org/lmacken/tbgrep
.. image:: https://coveralls.io/repos/lmacken/tbgrep/badge.png?branch=master
   :target: https://coveralls.io/r/lmacken/tbgrep
.. image:: https://pypip.in/v/tbgrep/badge.png
   :target: https://crate.io/packages/tbgrep
.. image:: https://pypip.in/d/tbgrep/badge.png
   :target: https://crate.io/packages/tbgrep

A module & command-line tool for extracting Python tracebacks from text.


Extracting tracebacks from bunch of files
-----------------------------------------

::

    $ tbgrep file1 file2 file3

Grepping for tracebacks in a pipeline
-------------------------------------

::

    $ tail -f logfile | tbgrep

Displaying all unique tracebacks ordered by the number of occurrences
---------------------------------------------------------------------

::

    $ tbgrep --stats logfile
    [...]

    == 99 occurences ==================================================

    Traceback (most recent call last):
     File "/usr/lib/python2.4/site-packages/bodhi/admin.py", line 209, in _masher_request
       req_params=kwargs)
     File "/usr/lib/python2.4/site-packages/fedora/client/proxyclient.py", line 285, in send_request
       raise AuthError(_('Unable to log into server.  Invalid'
    AuthError: Unable to log into server.  Invalid authentication tokens.  Send new username and password

    ==================================================================
    733 unique tracebacks extracted

Using the Python API
--------------------

Once instantiated, you pass each line to the `process` method, which will
return either None, or a string of a traceback.

>>> from tbgrep import TracebackGrep

>>> extractor = TracebackGrep()
>>> for line in file('logfile'):
>>>     tb = extractor.process(line)
>>>     if tb:
>>>         print tb

Instead of displaying each traceback found in the file, tbgrep also
supports generating statistics about all tracebacks in the file.

>>> extractor = TracebackGrep(stats=True)
>>> for line in file('logfile'):
>>>     extractor.process(line)
>>> extractor.print_stats()

Supported Input Formats
-----------------------

tbgrep can extract tracebacks from logs of various formats. For example,
CherryPy starts the traceback on a line with other details (like module,
timestamp, etc), but the rest of the trace starts at the beginning of the line.
Apache logs, on the other hand, will prefix each line of the traceback with
this information. tbgrep is designed to these kinds of situations
