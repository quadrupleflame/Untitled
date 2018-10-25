from flask_restful import Resource
from .model.hate_speech import process
from flask import request


class Test(Resource):
    def get(self, test_val):
        return {'test': 'Hello World, test_val:{}'.format(test_val)}


class URLAnalysis(Resource):
    def post(self):
        body = request.form.get('url')
        print(body, type(body))
        try:
            result = {'output': process.analyze_content(body)}
        except AssertionError:
            result = {'status': 0, 'info': 'TypeError'}
        except KeyError:
            result = {'status': 0, 'info': 'KeyError'}
        else:
            result['status'] = 1
        return result
