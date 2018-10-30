# ASE Untitled project

## How to run

```bash
python run_flask.py

# Do not use flask run
```

## Sample request
POST: localhost:5000/api/url

body:
```
url: https://en.wikipedia.org/wiki/Twitter
```

GET: localhost:5000/api/test/test

## Auth
all api require password and username in authorization header. Use Http Basic Auth now.

## TODO

1. implement more functionality in app/rest.py
2. implement login and logout system in auth.py and home.py, I guess if user could get an overview in 
his home page would be great. As well as register part. Right now this part is totally same with falskr,
flask official tutorial.
3. unit test
4. implement dockerfile, CI, server config etc..

## Requirements:
Use python 2.7

see requirements.txt

install all requirements by
```bash
pip install -r requirements.txt
```

set sqlite
```bash
flask init-db
```

## Error and fix
- run following
```python
import nltk
nltk.download('all')  
```


- textstat error 
located in textstat base folder

```python
from .textstat import textstat


__version__ = (0, 5, 0)


for attribute in dir(textstat):
    if callable(getattr(textstat, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(textstat, attribute)

```


## Credit
The nlp part is from https://github.com/t-davidson/hate-speech-and-offensive-language.git