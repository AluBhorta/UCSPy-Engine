# UCSPy-Engine

Python Prototype of UCSP Engine by AluBhorta.

## Deps

-   Python 3.6
-   virtualenv
-   Necessary python modules are listed in `requirements.txt`. Follow the usage guide.

## Usage

-   initialize new python 3.6 environment with virtualenv

```bash
virtualenv -p <path-to-python3.6> .env

# for example on a *NIX system
virtualenv -p $(which python3.6) .env
```

-   install the requirements

```bash
pip install -r requirements.txt
```

-   update `driver.py` main function according to your requirements and run it.

```bash
python driver.py
```
