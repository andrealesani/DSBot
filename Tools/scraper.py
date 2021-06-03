from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from googlesearch import search

session = requests.Session()
response = session.get('https://google.com')
print(session.cookies)
headers = {
'authority': 'scrapeme.live',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-user': '?1',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

query = input('query >> ')

links = search(query, num_results=100)
print(links)
for l in links[1:]:
    print(l)
    try:
        response = requests.get(l, {"User-Agent": UserAgent().random}, cookies=session.cookies, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.find_all(text=True)

        outputs = []
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head',
            'input',
            'script',
            'style',
            'link',
            'table',
            'href',
            'a',
            'img',
            'li',
            'footer',
            'span',
            'ul',
            'picture',
            'button',
            'form',
            'select',
            'option',
            'clippath',
            'svg',
            'g',
            'nav',
            'defs',
            'label'
            # there may be more elements you don't want, such as "style", etc.
        ]
        for t in text:
            if t.parent.name not in blacklist:
                print(t.parent.name)
                if t.strip().startswith('<'):
                    pass
                #output += '{} '.format(t)
                else:
                    outputs.append(t.strip())

        #print(output)
        sentences = [i for i in outputs if query in i.lower()]
        #print(sentences)

        with open('sentences_scraped_{}.txt'.format(query), 'a') as f:
            for i in sentences:
                f.write(i+'\n')
    except requests.exceptions.Timeout as e:
        # Maybe set up for a retry
        print(e)
    except:
        # Maybe set up for a retry
        print('Error link')

