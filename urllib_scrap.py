import nltk
import urllib
import bs4 as bs
import re
from nltk.corpus import stopwords
nltk.download("stopwords")

source = urllib.request.urlopen("https://en.wikipedia.org/wiki/Virat_Kohli")

soup = bs.BeautifulSoup(source, features="html.parser")

text= ""
for para in soup.find_all('p'):
    text+=para.text
# print(text)


text = re.sub(r'\[[0 -9]*\]', ' ', text)  ### removes number
text = re.sub(r'\s+',' ', text)      ### removes spaces
text = text.lower()

nltk.download("punkt")
sentences= nltk.sent_tokenize(text)

for s in sentences:
    print(s)
