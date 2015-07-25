Sage Dev Webapp
===============

Quickstart
----------

1. Install dependencies using

       $ ./bootstrap.sh

2. Set paths

       $ source activate

3. Run the dev server

       $ gulp serve


File layout
-----------

* ``app``: Python backend source
* ``www``: Frontend source code (Polymer)
* ``test_app``: Unit testing for Python code



Development
-----------

All interesting operations are configured as gulp tasks, similar
to makefile targets. Available options are:


* ``gulp serve``                Build & run the dev server

* ``gulp python:test``          Run the Python unittest
