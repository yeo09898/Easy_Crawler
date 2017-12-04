#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 11:03:48 2017

@author: jackylee
"""
from bs4 import BeautifulSoup
import re
import time
import requests
import datetime
import csv


def getLink(link):
    source = link.get('href')
    if '/biz' in source:
        source = "https://www.yelp.com" + source
        source = source.split('?osq=')[0].strip()
        print (source)
    else:
        source = 'NA'
    return source


def getTitle(tag):
    span = tag.find('span')
    title = span.text
    return title


def run_search(url, time_limit):
    start_time = datetime.datetime.now()
    p = -1
    csv_lst = list()

    fw = open('restaurant.txt', 'w+')
    with fw:

        while (True):
            p = p + 1
            running_time = datetime.datetime.now() - start_time
            if running_time.seconds / 60.0 > time_limit:
                print("time out")
                break
            print ('page', p)
            html = None

            pageLink = url + str(p * 10)

            for i in range(5):
                try:
                    running_time = datetime.datetime.now() - start_time
                    if running_time.seconds / 60.0 > time_limit:
                        print("time out")
                        break

                    response = requests.get(pageLink, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html = response.content
                    break
                except Exception as e:
                    print ('failed attempt', i)
                    time.sleep(0.1)

            if not html: continue

            soup = BeautifulSoup(html.decode('ascii', 'ignore'), 'lxml')

            restaurant_list = soup.findAll('div', {'class': re.compile('main-attributes')})
            print("reading data...\n")
            for restaurant in restaurant_list:
                running_time = datetime.datetime.now() - start_time
                if running_time.seconds / 60.0 > time_limit:
                    print("time out")
                    break

                link = restaurant.find('a', {'class': re.compile('biz-name js-analytics-click')})
                source = getLink(link)
                title = getTitle(link)
                category = get_category(restaurant)
                rating = get_rating(restaurant)

                if source == 'NA':
                    continue
                fw.write(title + "\n" + category + "\n" + rating + "\n" + source + "\n")
                csv_lst.append((title, category, rating, source))

                time.sleep(0.1)

        fw.close()
        write_csv(csv_lst)


def get_rating(tag):
    ratingChunk = tag.find('div', {'class': "i-stars"})
    rating = ratingChunk.get('title')
    return rating


def get_category(tag):
    cate_Chunk = tag.find('span', {'class': "category-str-list"}).findAll('a')
    category = ""
    for cate in cate_Chunk:
        category = cate.text + " "
    return category.strip()


def write_csv(all_result):
    with open('doc/result.csv', 'w+') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(("Title", "Category", "Rating", "Link"))
        for i in all_result:
            f_csv.writerow(i)
        f.close()


def run(keyword, time_limit):
    url = 'https://www.yelp.com/search?find_desc=' + keyword + '&find_loc=New+York,+NY&start='
    run_search(url, time_limit)

