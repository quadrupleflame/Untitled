from classifier import *
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


def Analyze_content(str):
    html = urlopen(str)
    soup = BeautifulSoup(html.read())
    data=[]
    for string in soup.strings:
        string = " ".join(re.split("[^a-zA-Z.,!?]*", string.lower())).strip()
        data.append(string)
    return get_tweets_predictions(data)


if __name__ == '__main__':
    result = Analyze_content("https://en.wikipedia.org/wiki/Twitter")
    print result
    count = 0
    for i in result:
       count = count+1
       if i!=2:
           print i,count
