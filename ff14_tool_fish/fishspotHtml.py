import requests
from pyquery import PyQuery as pq
import re
import time
import pymysql
import os
from pathlib import Path

def write_to_file(filename, con):
    file_object = open(filename, 'w', encoding='utf-8')
    file_object.write(con)
    file_object.close()

url='https://cn.ff14angler.com/index.php'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
f = requests.get(url,headers=headers)
html = f.text
html.encode('utf-8')
ff=pq(html)
sel=ff('select[name=spot]').find('option').items()
path = "F:/htmls/fish_area/"
for i in sel:
    id=i.attr('value')
    if id=='0':
        continue
    id_file = Path(path + id + ".html")
    if id_file.exists():
        continue
    print(id)
    url1='https://cn.ff14angler.com/spot/'+id
    print(url1)
    html1 = requests.get(url1).text
    html1.encode('utf-8')
    my_file = Path(path)
    if my_file.exists():
        write_to_file(path + id + ".html", html1)
