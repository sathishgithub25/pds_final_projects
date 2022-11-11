#To import libraries
from json import load
from glob import glob
from collections import Counter
import operator
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
from statistics import multimode,mode


#  To read multiple json files and concatenate them into a single dataframe
def get_files():
    filepath = "data/isbi2022"
    all_files = [] # an empty list to store the data frames
    for root, dirs, files in os.walk(filepath):
        files = glob(os.path.join(root,'*.json'))
        for f in files:  
            all_files.append(os.path.abspath(f))
    # print(all_files)
    alist = []
    for i in all_files:
        with open(i, mode='r', encoding='utf-8') as doc:
            data = json.load(doc)
            alist.append(data)
    df = pd.DataFrame(alist)
    p = df.head()
    df.iloc[:4].to_json('single_df.json', orient="records", indent=4)
    df1 = pd.read_json("single_df.json")
    d = df1.head()
    print(d)
# get_files()

# To load the json file
data_file = load(open("data\isbi2022\page1.json", mode='r', encoding='utf-8'))
stopwords = list(map(lambda x: x.strip(), open("data/stopwords.txt", mode='r', encoding='utf-8').readlines()))


# ********** top 10 downloaded papers **********

def top_10_downloaded():
    all_titles = dict()
    a = data_file['records']
    # a = a[4:313]
    for b in a:
        c = b['articleTitle']
        d = b['downloadCount']
        all_titles[c] = d
    # print (all_titles)
    d = all_titles
    sorted_titles_list = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))
    top_10_downloaded = dict(itertools.islice(sorted_titles_list.items(),10))
    # print(len(top_10_downloaded))
    fig, ax = plt.subplots()
    bars =ax.barh(*zip(*top_10_downloaded.items()))
    ax.bar_label(bars)
    ax.set_xlabel('Download Count')
    ax.set_title('TOP 10 DOWNLOADED PAPERS')
    plt.show()


# ********** top 10 Cited papers **********

def top_10_cited():
    data_file = load(open("data\isbi2022\page1.json", mode='r', encoding='utf-8'))
    all_titles = dict()
    a = data_file['records']
    # a = a[4:313]
    for b in a:
        c = b['articleTitle']
        d = b['citationCount']
        all_titles[c] = d
    # print (all_titles)
    d = all_titles
    sorted_titles_list = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))
    top_10_cited = dict(itertools.islice(sorted_titles_list.items(),10))
    # print(len(top_10_cited))
    fig, ax = plt.subplots()
    bars =ax.barh(*zip(*top_10_cited.items()))
    ax.bar_label(bars)
    ax.set_xlabel('Number of citations')
    ax.set_title('TOP 10 cited papers')
    plt.show()


# ********** Mean of authors per paper **********

def authors_mean():
    all_authors = []
    a = data_file['records']
    st = len(a)
    a = a[4:st-1]
    for b in a:
        c = b['authors']
    # print(len(c))
        for d in c:
            e = d['preferredName']
            all_authors.append(e)
    # print(len(all_authors))
    mean_authors = int(len(all_authors)/len(a))
    print(mean_authors)


# ********** average number of pages per paper **********

def avg_pages():
    all_pages = []
    a = data_file['records']
    st = len(a)
    a = a[4:st-1]
    for b in a:
        # c = b['articleTitle']
        d = b['endPage']
        all_pages.append(d)
    all_pages = [eval(i) for i in all_pages]
    avg_pages = int(sum(all_pages)/len(all_pages))
    print(avg_pages)


# *********** most used words in the abstract ***********

def word_cloud():
    all_words = []
    final_out = []
    a = data_file['records']
    st = len(a)
    a = a[4:st-1]
    for b in a:
        c = b['abstract']
        words = c.split(" ")
        all_words = all_words + words
    final_out = [i for i in all_words if i not in stopwords]
    # print(len(final_out))
    word_list = dict(Counter(final_out))
    d = word_list
    sorted_word_list = dict( sorted(d.items(), key=operator.itemgetter(1),reverse=True))

    # visualizing as wordcloud
    wordcloud = WordCloud(width = 1000, height = 500,background_color="white",random_state=1, colormap='rainbow').generate_from_frequencies(sorted_word_list)
    plt.figure(figsize=(11,8))
    plt.imshow(wordcloud)
    plt.title(label="\'Most used words\'", fontsize=40)
    plt.axis('off')
    plt.show()

# '******** Author who contributed most papers *******'
def get_author():
    all_authors = []
    a = data_file['records']
    st = len(a)
    a = a[4:st-1]
    for b in a:
        c = b['authors']
        for d in c:
            e = d['preferredName']
            all_authors.append(e)
    
    # print(multimode(all_authors))

    word_cloud_dict=dict(Counter(all_authors))
    # print(word_cloud_dict)
    wordcloud = WordCloud(width = 1000, height = 500,background_color="black",random_state=1).generate_from_frequencies(word_cloud_dict)
    plt.figure(figsize=(11,8))
    plt.imshow(wordcloud)
    plt.title(label="\'Author who contributed most papers\'", fontsize=20)
    plt.axis('off')
    plt.show()


# top_10_downloaded()
# top_10_cited()
# authors_mean()
# avg_pages()
# word_cloud()
# get_author()