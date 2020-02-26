# UCSPy-Engine

Python Prototype of UCSP Engine by AluBhorta.

## Deps

-   Python 3.6
-   virtualenv


## Usage

initialize and activate new `python 3.6` environment with virtualenv (for gnu/linux systems)

```bash
virtualenv -p <path-to-python3.6> .env

virtualenv -p $(which python3.6) .env

source .env/bin/activate
```

install the requirements using pip

```bash
pip install -r requirements.txt
```

update the `main` function of `driver.py` according to your requirements and run it.

```bash
python driver.py
```

## Todo 

* add `args parser` for running
* input components could be parsed and stored in memory/cache via redis
