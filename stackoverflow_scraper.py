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
import re
import datetime
import csv

PAGECOUNT = 100


# for search
def getLink_Title(tag):
    sourceChuck = tag.find('div', {'class': 'summary'})
    source = sourceChuck.find('a', {'href': re.compile('/questions')})
    link = source.get('href')
    if '/questions' in link:
        link = "https://stackoverflow.com" + link
        title = str(source.text.encode('utf-8').strip())
    else:
        link = 'NA'
        title = 'NA'
    return link, title


# for single_keyword
def single_Link_Title(tag):
    sourceChuck = tag.find('div', {'class': 'summary'})
    source = sourceChuck.find('h3').find('a')
    link = source.get('href')
    if '/questions' in link:
        link = "https://stackoverflow.com" + link
        title = str(source.text.encode('utf-8').strip())
        print (title)
    else:
        link = 'NA'
        title = 'NA'
    return link, title


def single_getContent(tag):
    sourceChuck = tag.find('div', {'class': 'summary'})
    source = sourceChuck.find('div', {'class': 'excerpt'})
    content = str(source.text.encode('utf-8').strip())
    content = re.sub(r'\\n', " ", content)
    content = re.sub(r'\\r', "", content)

    return content


def getVote(tag):
    sourceChuck = tag.find('span', {'class': 'vote-count-post'})
    source = sourceChuck.find('strong').text

    return source


def getStatus(tag):
    sourceChuck = tag.find('div', {'class': 'stats'})
    source = sourceChuck.find('div', {'class': 'status'})
    if source:
        status = source.get('class')
    else:
        source = sourceChuck.find('div', {'class': 'votes'})
        status = source.get('class')

    return status[1]


def getAnswerNum(tag):
    sourceChuck = tag.find('div', {'class': 'stats'})
    source = sourceChuck.find('div', {'class': 'status'})
    num = 0
    if source:
        num = source.find('strong').text

    return num


def run_search(url, keyword, time_limit):
    start_time = datetime.datetime.now()
    csv_lst = list()

    PROCESS = 0
    p = 0
    fw = open('doc/outputs.txt', 'w+')
    with fw:
        fw.write("Title\t\tLink\t\tVote\t\tStatus\t\tAnswerNumber\n")

        while(True):
            p = p + 1
            running_time = datetime.datetime.now() - start_time
            if running_time.seconds / 60.0 > time_limit:
                print("time out")
                break


            print ('page', p)
            fw.write("page" + str(p) + '\n')
            html = None

            pageLink = url + str(p) + '&tab=Relevance&pagesize=50&q=' + keyword

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

            tags = soup.findAll('div', {'class': re.compile('question-summary search-result')})
            print("reading data...\n")
            for tag in tags:
                running_time = datetime.datetime.now() - start_time
                if running_time.seconds / 60.0 > time_limit:
                    print("time out")
                    break

                vote = getVote(tag)
                status = getStatus(tag)
                answer_num = getAnswerNum(tag)
                link, title = getLink_Title(tag)
                fw.write(title + "\n" + link + "\n" + str(vote) + "\n" + status + "\n" + str(answer_num) + "\n")
                fw.write("\n")

                csv_lst.append((title, link, vote, status, answer_num))

                PROCESS += 1
                print (PROCESS)

                time.sleep(0.1)
            time.sleep(1)

        fw.close()
        write_csv(csv_lst)


def single_key(url, frame, time_limit):
    start_time = datetime.datetime.now()
    csv_lst = list()

    PROCESS = 0
    p = 0
    fw = open('doc/outputs.txt', 'w+')
    with fw:
        fw.write("Title\t\tContent\t\tLink\t\tVote\t\tStatus\t\tAnswerNumber\n")

        while(True):
            p = p + 1
            running_time = datetime.datetime.now() - start_time
            if running_time.seconds / 60.0 > time_limit:
                print("time out")
                break

            print ('page', p)
            fw.write("page" + str(p) + '\n')
            html = None

            pageLink = url + frame + '?page=' + str(p) + '&sort=votes&pagesize=50'

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
            tags = soup.findAll('div', {'class': re.compile('question-summary')})

            print("reading data...\n")

            for tag in tags:
                running_time = datetime.datetime.now() - start_time
                if running_time.seconds / 60.0 > time_limit:
                    print("time out")
                    break

                vote = getVote(tag)
                status = getStatus(tag)
                answer_num = getAnswerNum(tag)
                link, title = single_Link_Title(tag)
                content = single_getContent(tag)

                fw.write(
                    title + "\n" + content + "\n" + link + "\n" + str(vote) + "\n" + status + "\n" + str(answer_num) + "\n")
                fw.write("\n")
                csv_lst.append((title, link, vote, status, answer_num, content))

                PROCESS += 1
                print (PROCESS)

                time.sleep(0.1)
            time.sleep(1)

        fw.close()
        write_csv(csv_lst)


def get_review_rating(tag):
    ratingChunk = tag.find('meta', {'itemprop': "ratingValue"})
    rating = ratingChunk.get('content')
    print (rating)

    reviewChunk = tag.find('p', {'itemprop': "description"})
    if reviewChunk and str(reviewChunk).strip():
        review = reviewChunk.text
        print (review)
    else:
        review = 'NA'
    rating = str(rating).strip()
    review = str(review).strip()
    return rating, review


def get_link_list(filename):
    f = open(filename, 'r')

    linklst = list()
    with f:
        lines = f.readlines()
        for line in lines:
            linklst.append(line.strip())
        f.close()
    return linklst


def write_csv(all_result):
    with open('doc/result.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(("Title","Link","Vote","Status","AnswerNumber","Content"))
        for i in all_result:
            f_csv.writerow(i)
        f.close()


def run(keyword, time_limit):
    if " " in keyword or "," in keyword:
        #     settings
        url = 'https://stackoverflow.com/search?page='
        run_search(url, keyword, time_limit)
    else:
        url = 'https://stackoverflow.com/questions/tagged/'
        single_key(url, keyword, time_limit)

