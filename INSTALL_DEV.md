# Development installation instructions

It is best to use a virtual environment for development work on smartcontainers. The pip virtualenvrionment wrapper package provides an convenient method to manage python virtual environments. Assuming you are using wrappers.

```bash
mkvirtualenv sc
pip install --editable .
pip install -r requirements_dev.txt
```

Note. Smart Containers requires that docker also be installed and in your shell's path.

