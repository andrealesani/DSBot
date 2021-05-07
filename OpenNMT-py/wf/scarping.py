import pandas as pd
import requests
from bs4 import BeautifulSoup

def href(soup):
    # get all href links from one page
    href=[]
    for i in soup.find_all("a",class_="question-hyperlink",href=True):
        href.append(i['href'])
    return href

def clean_empty_hrefs(hrefs):
   # remove all empty lists
    list_hrefs=[]
    for i in hrefs:
        if i!=[]:
            list_hrefs.append(i)
    # merge all elemenets in one list
    herfs_list=[]
    for i in list_hrefs:
        for j in i:
            herfs_list.append(j)
    return herfs_list

def add_prefix(herfs_list):
    # rearrage those links who do not have 'https://stackoverflow.com' prefix
    new_href=[]
    prefix='https://datascience.stackexchange.com'
    for h in herfs_list:
        if 'https' not in h:
            m=prefix+h+"answertab=votes#tab-top"
            new_href.append(m)
        else:
            new_href.append(h+"answertab=votes#tab-top")
    return new_href


def single_page_scraper(url):
    req = requests.get(url=url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup
def single_page_question_answer(url):
    page = single_page_scraper(url).find_all("div", class_="post-text", itemprop="text")
    question = [i.find("p").get_text() for i in page][0]
    answer = [i.find("p").get_text() for i in page][1:3]

    return question, answer


import itertools


def questions_answers(start_page, end_page):
    soups = []
    for page in range(start_page, end_page):
        req = requests.get(
            url='https://datascience.stackexchange.com/search?q=%5bk-means%5d'.format(page))
        soup = BeautifulSoup(req.text, "html.parser")
        soups.append(soup)
    #print(soups)
    print("Soups are ready!")
    # obtain all href
    hrefs = []
    for soup in soups:
        hrefs.append(href(soup))


    herfs_list = clean_empty_hrefs(hrefs)
    new_hrefs_list = add_prefix(herfs_list)
    print(new_hrefs_list)
    print("All hrefs are ready!")
    quesitons = []
    answers = []
    for url in new_hrefs_list:
        try:
            q, a = single_page_question_answer(url)
            quesitons.append(q)
            answers.append(a)
        except:
            pass
    print("quesitons and answers are ready!")

    new_answers = []
    for i in range(len(answers)):
        try:
            new_answers.append(answers[i][0])
        except:
            new_answers.append(None)
    print("All most done!")
    new_q = []
    new_a = []
    merge_answer = list(itertools.chain.from_iterable(answers))
    for i in range(len(merge_answer) - 1):
        new_q.append(merge_answer[i])
        new_a.append(merge_answer[i + 1])

    return quesitons + new_q, new_answers + new_a


Questions,Answers=questions_answers(1,5)
print(Questions)
print(Answers)

import requests
from bs4 import BeautifulSoup

url = 'https://stackexchange.com/questions?pagesize=50'
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'lxml')

links = []
for link in soup.find_all('a'):
    links.append((link.get('href')))

import re
question_links = [k for k in links if k and 'questions' in k]
pattern = re.compile('questions/\d')
question_links = filter(pattern.search, question_links)
question_links = list(set(question_links))


def populate_question_links(url='https://stackexchange.com/questions?pagesize=50'):
    '''Generates a list of URLs pointing to 'hot questions' on the Stack Exchange network. No non-optional arguments.'''

    r = requests.get(url)  # HTTP request
    html_doc = r.text  # Extracts the html
    soup = BeautifulSoup(html_doc, 'lxml')  # Create a BeautifulSoup object

    links = []
    for link in soup.find_all('a'):
        links.append((link.get('href')))

    question_links = [k for k in links if k and 'questions' in k]  # Filter links that contain the string 'questions'

    pattern = re.compile('questions/\d')  # Create pattern to search for

    question_links = filter(pattern.search,
                            question_links)  # Filter links which are questions and also followed by a numerical ID
    question_links = list(set(question_links))  # Remove duplicates

    return (question_links)

def find_cat(url):
    '''Returns the category from Stack Exchange question url'''
    return(url.split("https://")[1].split(".")[0])
import numpy as np
from random import randint
from time import sleep

def get_text(url, rm_digits=True, rm_punct=True, pause=False, sleep_max=5):
    '''Outputs the text of a question from a Stack Exchange URL. Outputs np.NaN in case of error'''
    if pause == True:
        sleep(randint(1, sleep_max))
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'lxml')

    digit_list = "1234567890"
    punct_list = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    try:
        text = soup.find(attrs={'class': 'post-text'}).get_text()
        text = text.replace('\n', ' ')
        if rm_punct == True:
            for char in punct_list:
                text = text.replace(char, "")
        if rm_digits == True:
            for char in digit_list:
                text = text.replace(char, "")
        return (find_cat(url), text)
    except:
        return (np.NaN, np.NaN)


def create_stackexchange_url(category, ID):
    '''Concatenates Stack Exchange category and ID to form Stack Exchange URL'''
    return ('https://' + category + '.stackexchange.com/questions/' + str(ID))


def fetch_cat_and_id(url):
    '''Returns the question ID and category of an inputed Stack Exchange question URL. Inverse of create_stackexchange_url'''
    url = url.split('/')
    ID = url[4]
    cat = url[2].split('.')[0]
    try:
        int(ID)
    except ValueError:
        print("Unexpected URL input. ID retrieved is not an integer")
    return (cat, ID)


def find_cat(url):
    '''Returns the category from stack exchange question url'''
    return (url.split("https://")[1].split(".")[0])


def back_generate_links(question_links, n=100):
    # question_links should include 1 link per category to ensure balanced classes
    new_links = []
    for link in question_links:
        cat, ID = fetch_cat_and_id(link)
        for i in range(n):
            new_ID = int(ID) - i
            new_links.append(create_stackexchange_url(cat, new_ID))
    return (new_links)

text = soup.find(attrs={'class':'post-text'}).get_text()

