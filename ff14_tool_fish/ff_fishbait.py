import re
import requests
from pyquery import PyQuery as pq
import pymysql

conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='1234',database='ff14',charset='utf8mb4')
cur=conn.cursor()

# for v in range(1,7):
url="https://ff14angler.com/index.php?lang=cn&list=bait&page=7"#+str(v)
html = requests.get(url).text
html.encode('utf-8')
ff=pq(html)
sel=ff('.list').find('tr').items()
for i in sel:
    id = re.findall(r'<a href="/bait/([0-9]*)">', i.html())
    if len(id) ==0:
        continue
    name=re.findall(r'</span>(.*?)</a></td>',i.html())
    lv = i.find('.ilevel').text()
    sql="INSERT INTO `ff_fish_bait` (`bait_id`, `bait`, `level`) VALUES ('"+''.join(id)+"', '"+''.join(name)+"', '"+lv+"')"
    cur.execute(sql)
    conn.commit()
    print(sql)
cur.close()
conn.close()