
import json
from json import load
import pandas as pd
import os
from glob import glob
from collections import Counter
import operator


def get_files():
    filepath = "data/isbi2022"
    all_files = [] # an empty list to store the data frames
    for root, dirs, files in os.walk(filepath):
        files = glob(os.path.join(root,'*.json'))
            # print(files)
        for f in files:  
            all_files.append(os.path.abspath(f))
    # print(all_files)
    alist = []
    for i in all_files:
        with open(i, mode='r', encoding='utf-8') as doc:
            data = json.load(doc)
            alist.append(data)
    # print(alist[:2])
    df = pd.DataFrame(alist)
    p = df.head()
    # print(p)
    df.iloc[:4].to_json('df_indent.json', orient="records", indent=4)
    df1 = pd.read_json("df_indent.json")
    d = df1.head()
    # print(df1)
# get_files()

#top 10 downloaded papers
data_file = load(open("df_indent.json", mode='r', encoding='utf-8'))
def top_10():
    b = []
    f = []
    for adic in data_file:
        b.append(adic)
    # print(len(b))
        for c in b:
            d = c['records']
        # print(len(d))
            for e in d:
                f = e['authors']
        print(len(f))
    #         for g in f:
    

top_10()