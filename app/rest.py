from flask_restful import Resource
from .model.hate_speech import process
from flask import request
from .auth import auth
from flask_httpauth import HTTPBasicAuth
from .db import get_db
from auth import check_password_hash

#auth = HTTPBasicAuth()

'''
@auth.verify_password
def verify_password(username, password):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    error = None
    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    return error is None
'''

class Test(Resource):
    decorators = [auth.login_required]
    #@auth.login_required
    def get(self, test_val):
        return {'test': 'Hello World, test_val:{}'.format(test_val)}

class URLAnalysis(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(URLAnalysis, self).__init__()
        self.model = process.Analyzer()

    def get(self):
        # TODO get should return an instruction of how to post
        return 'Developing'

    #@auth.login_required
    def post(self):
        body = request.form.get('url')
        try:
            result = {'output': self.model.get_url_predictions(body)}
        except AssertionError:
            result = {'status': 0, 'info': 'TypeError'}
        except KeyError:
            result = {'status': 0, 'info': 'KeyError'}
        except Exception:
            result = {'status': 0, 'info': 'Error'}
        else:
            result['status'] = 1
        return result


class TextAnalysis(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        super(TextAnalysis, self).__init__()
        self.model = process.Analyzer()

    def get(self):
        # TODO get should return an instruction how to use post
        return 'Developing'

    @auth.login_required
    def post(self):
        body = request.form.get('text')
        try:
            result = {'output': self.model.get_text_predictions(body)}
        except AssertionError:
            result = {'status': 0, 'info': 'TypeError'}
        except KeyError:
            result = {'status': 0, 'info': 'KeyError'}
        except Exception:
            result = {'status': 0, 'info': 'Error'}
        else:
            result['status'] = 1
        return result


class TextMask(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.model = process.WordMasker()

    def get(self):
        return 'Developing'

    @auth.login_required
    def post(self):
        body = request.form.get('text')
        try:
            result = {'output': self.model.get_masked_text(body)}
        except AssertionError:
            result = {'status': 0, 'info': 'TypeError'}
        except KeyError:
            result = {'status': 0, 'info': 'KeyError'}
        except Exception:
            result = {'status': 0, 'info': 'Error'}
        else:
            result['status'] = 1
        return result
