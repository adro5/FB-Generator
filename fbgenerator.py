# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:53:41 2018

@author: Adam Robinson
"""

import pandas as pd
import tkinter as tk
import urllib.request
import urllib.parse
import re
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

year1 = pd.read_csv(filedialog.askopenfilename(filetypes=(("csv UTF-8 files", "*.csv"),)))
year2 = pd.read_csv(filedialog.askopenfilename(filetypes=(("csv UTF-8 files", "*.csv"),)))
merged_tbl = year1.merge(year2, how="outer")
"""print(merged_tbl)"""
merged_tbl.to_csv("merged_data.csv", index=False)
merged_tbl = merged_tbl.dropna(axis=1)

selected_data = merged_tbl.loc[0:, 'Date':'Opp']

selected_data['Score Diff'] = pd.Series(selected_data['Pts'] - selected_data['Opp'], index=selected_data.index)
selected_data['Total Score'] = pd.Series(selected_data['Pts'] + selected_data['Opp'], index=selected_data.index)
selected_data['RVal'] = pd.Series((2*selected_data['Score Diff']) + (selected_data['Total Score']/(2*selected_data['Score Diff'])), index=selected_data.index)
    
selected_data.sort_values(['RVal','Opponent'],kind='mergesort',inplace=True)

print(selected_data)
selected_data.to_csv("final_rank.csv", index=False)

for i, row in selected_data.iterrows():
    strFBq = row[2] + " " + row[3]
    query_string = urllib.parse.urlencode({"search_query" : strFBq})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("http://www.youtube.com/watch?v=" + search_results[0])



