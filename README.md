# ASE Untitled project

## How to run

```bash
python run_flask.py

# Do not use flask run
```

## Requirements:
see requirements.txt

## Error and fix
- run following
```
  >>> import nltk
  >>> nltk.download('stopwords')
  Searched in:
    - 'C:\\Users\\Pengyu Chen/nltk_data'
    - 'C:\\nltk_data'
    - 'D:\\nltk_data'
    - 'E:\\nltk_data'
    - 'C:\\Miniconda3\\envs\\ase\\nltk_data'
    - 'C:\\Miniconda3\\envs\\ase\\share\\nltk_data'
    - 'C:\\Miniconda3\\envs\\ase\\lib\\nltk_data'
    - 'C:\\Users\\Pengyu Chen\\AppData\\Roaming\\nltk_data'
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

- run this

```python
import nltk
nltk.download('averaged_perceptron_tagger')
```

## Credit
The nlp part is from https://github.com/t-davidson/hate-speech-and-offensive-language.git