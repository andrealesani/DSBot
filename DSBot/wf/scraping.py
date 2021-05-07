import wikipedia
import re
import string
import re
from scipy import sparse as sp_sparse
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
import urllib
import requests
from bs4 import BeautifulSoup

query = "pca"
query = query.replace(' ', '+')
URL = f"https://google.com/search?q={query}"
# desktop user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
headers = {"user-agent" : USER_AGENT}
resp = requests.get(URL, headers=headers)
if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
results = []
for g in soup.find_all('div', class_='r'):
    anchors = g.find_all('a')
    if anchors:
        link = anchors[0]['href']
        title = g.find('h3').text
        item = {
            "title": title,
            "link": link
        }
        results.append(item)
print(results)
'''
# Specify the title of the Wikipedia page
wiki = wikipedia.page('k-means clustering')
# Extract the plain text content of the page
text = wiki.content
# Clean text
text = re.sub('\[\d+\]', '', text)
text = re.sub(r'==.*?==+', '', text)
text = text.replace('\n', '')
text = text.replace('\t', '')
text = text.replace('                        ','')
text = text.replace('        ','')
text = text.replace('   ','')
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
print(STOPWORDS)

def text_prepare(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower()
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text)
    #text = re.sub(BAD_SYMBOLS_RE, "", text)
    text = " ".join([word for word in text.split() if not word in STOPWORDS])
    return text
text=text_prepare(text)
print(text)

text = text.split('.')
text = [re.sub(BAD_SYMBOLS_RE, "", t) for t in text]
text = [t.lower().translate(str.maketrans('', '', string.punctuation)).strip() for t in text if t.lower().translate(str.maketrans('', '', string.punctuation)).strip()!='']

print(text)
print(len(text))
'''