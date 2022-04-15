# Simple pygubu application integration with Nuitka

Install nuitka

```bash
pip install Nuitka
```

Note: tested with Nuitka version 0.7.7

Build the application

```bash
python -m nuitka --enable-plugin=tk-inter --include-data-file=myapp.ui=myapp.ui --include-data-dir=./imgs=imgs --include-package=pygubu --show-progress --show-modules --standalone  myapp.py
```
