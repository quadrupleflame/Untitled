import app
# This line is important, DO NOT DELETE IT.
from app.model.hate_speech.classifier import tokenize as tokenize, preprocess


if __name__ == '__main__':
    flask_app = app.create_app()
    flask_app.run(debug=True)
