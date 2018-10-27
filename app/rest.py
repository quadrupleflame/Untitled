from flask_restful import Resource
from .model.hate_speech import process
from flask import request


class BaseResource(Resource):
    def HMAC_enocde(self):
        pass


class Test(Resource):
    def get(self, test_val):
        return {'test': 'Hello World, test_val:{}'.format(test_val)}


class URLAnalysis(Resource):
    def __init__(self):
        super(URLAnalysis, self).__init__()
        self.model = process.Analyzer()

    def get(self):
        # TODO get should return an instruction of how to post
        pass

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
    def __init__(self):
        super(TextAnalysis, self).__init__()
        self.model = process.Analyzer()

    def get(self):
        # TODO get should return an instruction how to use post
        pass

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
    def __init__(self):
        self.model = process.WordMasker()

    def get(self):
        return 'Developing'

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
