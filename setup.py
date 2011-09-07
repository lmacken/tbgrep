from setuptools import setup, find_packages
import sys, os

version = '0.1.2'

f = open('tbgrep/README.rst')
long_description = f.read()
f.close()

setup(name='tbgrep',
      version=version,
      description="Extract Python Tracebacks from text",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Debuggers',
          'Topic :: Text Processing :: Filters',
          'Topic :: Utilities',
      ],
      keywords='',
      author='Luke Macken',
      author_email='lmacken@redhat.com',
      url='http://github.com/lmacken/tbgrep',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts' : [
              'tbgrep = tbgrep.commands:tbgrep',
          ],
      },
     )
