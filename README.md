Recursivley browse a directory and return all of the classes in all python files, with the doc string for that class. Currently classes only, no function docstrings.

## Install
```
python3 setup.py sdist bdist_wheel
pip3 install dist/*
```

## Quick Start:

##### Python:

`get_doc_strings(rootdir)` returns a dict of class names and there docstring

Add to python path:
```
from get_doc_strings import get_doc_strings
```

Call Function:
```
docstrings = get_doc_strings("/rel/or/abs/path/to/rootdir/to/search/from")
```

##### Command Line Interface:

Add to python path:
```
export PYTHONPATH=~/.local/lib/python3.8/site-packages/get_doc_strings
```

Args:
```
usage: get_doc_strings.py [-h] --dir DIR [-v]

optional arguments:
  -h, --help     show this help message and exit
  --dir DIR      The directory to recursivley search from
  -v, --verbose  Print debug messages
```

For example:
```
python3 -m get_doc_strings --dir .
```
