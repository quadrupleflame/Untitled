from classifier import get_tweets_predictions
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


def analyze_content(_str):
    _str = str(_str)
    assert isinstance(_str, str)
    html = urlopen(_str)
    soup = BeautifulSoup(html.read())
    data = []
    for string in soup.strings:
        string = " ".join(re.split("[^a-zA-Z.,!?]*", string.lower())).strip()
        data.append(string)
    return get_tweets_predictions(data).tolist()


if __name__ == '__main__':
    test_str = "https://en.wikipedia.org/wiki/Twitter"
    print type(test_str)
    result = analyze_content(test_str)
    print result
    count = 0
    for i in result:
        count = count + 1
        if i != 2:
            print i, count
