# map
This project is an interactive map of all issues catalogued in our map app

## Build
**Install virtual environment library**
```bash
cd <PROJECT_FOLDER_NAME>/
pip install virtualenv #if you don't have virtualenv installed
```

**Create virtualenv**
```bash
virtualenv <NAME_OF_VIRTUAL_ENVIRONMENT> #i.e. venv
```
***NOTE***
_The current latest version of numpy only supports up to Python 3.7. If you have any version of Python that's later, you'll have to install a Python 3.7 specific environment like so:_

```bash
virtualenv -p python3.7 <NAME_OF_VIRTUAL_ENVIRONMENT>
```

**Activate virtualenv**
```bash
source <NAME_OF_VIRTUAL_ENVIRONMENT>/bin/activate
```

**Install project requirements usings the requirements.text**
```bash
pip install -r requirements.txt
```

## Run
Run python script in root directory of your project to start
```
python main.py
```


Linter
```bash
pre-commit run --all-files
```
