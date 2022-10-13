import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import re
import os


def blogsite():
    '''
    
    '''
#     Set the URL
    url = 'https://codeup.com/blog/'    
#     Set the headers so that we don't get a 403
    headers = {'User-Agent': 'Codeup Data Science'}    
#     Cook the soup full of content
    soup = BeautifulSoup(get(url, headers=headers).content, features="lxml")    
#     Return the soup
    return soup


def get_blog_articles():
    '''
    
    '''
    filename = "codeup_blogs"
    
    # if file is available locally, read it
    if os.path.isfile(filename):
        return pd.read_pickle(filename)
    
    # if file not available locally, acquire data from inshorts.com/en/read
    # and write it as pickle locally for future use
    else:
    #     Set the headers so that we don't get a 403
        headers = {'User-Agent': 'Codeup Data Science'}
    #     Get space
        space = ' '

        list_o_dicts = []
    #     Get the soup
        soup = blogsite()

        blog_list = soup.find_all('h2', limit=6)

        for i in blog_list:

            title = i.text

            page = i.a['href']

            blog_page = BeautifulSoup(get(page, 'html.parser', headers=headers).content, features="lxml")

            content = ''

            date, tags = date_n_tags(blog_page.select('p')[0].text)

            for j in range(1, 4):

                par = blog_page.select('p')[j].text

                content += space

                content += par

            blog_dict = {'title': title,
                         'url': page,
                         'date': date,
                         'tags': tags,
                         'content': content
                        }

            list_o_dicts.append(blog_dict)

        pd.to_pickle(list_o_dicts, 'codeup_blogs')
        return list_o_dicts
            
        

def date_n_tags(string):
    '''
    
    '''
    
    regexp = r'(.{11})\s\|\s(.*)'
    
    date = re.sub(regexp, r'\1', string)
    
    tags = re.sub(regexp, r'\2', string)
    
    return date, tags

def get_all_shorts(base_url= 'https://inshorts.com/en/read'):
    '''
    
    '''
    filename = "inshorts_articles"
    
    # if file is available locally, read it
    if os.path.isfile(filename):
        return pd.read_pickle(filename)
    
    # if file not available locally, acquire data from inshorts.com/en/read
    # and write it as pickle locally for future use
    else:
        cats = get_cats(base_url)

        all_articles = []

        for cat in cats:

            cat_url = base_url + '/' + cat

            print(get(cat_url))

            cat_soup = soupify(get(cat_url).content)

            cat_titles = [title.text for title in cat_soup.find_all('span', itemprop='headline')]

            cat_bodies = [body.text for body in cat_soup.find_all('div', itemprop='articleBody')]

            cat_articles = [{'title': title,
                             'category': cat,
                             'body': body} for title, body in zip(cat_titles, cat_bodies)]

            print('cat articles length: ',len(cat_articles))

            all_articles.extend(cat_articles)

            print('length of all_articles: ', len(all_articles))

        pd.to_pickle(all_articles, 'inshorts_articles')
        return all_articles