## Installation (for dev)

```
python3 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Credits
This is a port of the prayer times program extracted from adhan-java: https://github.com/batoulapps/adhan-java in Python.
Credits go to the original author for the original implementation, especially the very complex astronomical formulas.
As it stands this project is very similar to and mirrors the structure of the original project but may gradually differ
through refactoring and in an effort to rewrite in a more pythonic way.