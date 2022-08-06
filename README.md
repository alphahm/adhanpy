# adhanpy

This is a port of [batoulapps/adhan-java](https://github.com/batoulapps/adhan-java), a prayer times program, from Java to Python.
As it stands the project reuses most of the structure of the original project but may differ through refactoring and in an effort
to rewrite in a more pythonic way where it makes sense.
Like the original project there is no external dependencies except for tests in development where `pytest` is made use of.

## Requirements

* Python >=3.9

## Example

Example is located in `src/example`. To run:

```
python src/example/main.py
```

## Development

To install adhanpy for development purposes, run the following:

```
python3 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Licence

MIT

## Credits

Credits go to the original author for the original implementation in java and other languages, especially the very complex astronomy
formulas.
