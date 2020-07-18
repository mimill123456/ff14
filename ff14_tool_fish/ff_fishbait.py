import re
import requests
from pyquery import PyQuery as pq
import ff14_tool_fish.fishinfo as fishinfo

delsql = "DELETE FROM `ff_fishbait`"
fishinfo.connecttomysql(delsql)
for v in range(1,6):
    url="https://cn.ff14angler.com/?list=bait&page="+str(v)
    html = requests.get(url).text
    html.encode('utf-8')
    ff=pq(html)
    sel=ff('ol[class=tile]').find('li').items()
    for i in sel:
        if len(i.find('a')) ==0:
            continue
        # print('%r' % i.find('a'))
        id = re.findall(r'<a href="/bait/(.*?)" title=".*?">', i.html())
        name=i.find('a').attr('title')
        lv = i.find('.ilevel').text()
        sql="INSERT INTO `ff_fishbait` (`bait_id`, `bait`, `level`) VALUES ('"+''.join(id)+"', '"+name+"', '"+lv+"')"
        fishinfo.connecttomysql(sql)
        print(sql)
exsql = "INSERT INTO `ff_fishbait` (`bait_id`, `bait`) VALUES ('2001', '大型叉')"
fishinfo.connecttomysql(exsql)
exsql2 = "INSERT INTO `ff_fishbait` (`bait_id`, `bait`) VALUES ('2002', '中型叉')"
fishinfo.connecttomysql(exsql2)
exsql3 = "INSERT INTO `ff_fishbait` (`bait_id`, `bait`) VALUES ('2003', '小型叉')"
fishinfo.connecttomysql(exsql3)

