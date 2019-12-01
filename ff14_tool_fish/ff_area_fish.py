import requests
import re
from pyquery import PyQuery as pq
import fishinfo
import pymysql
# conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='1234',database='ff14',charset='utf8mb4')
# cur=conn.cursor()
sql=[]
for v in range(1,13):
    url="https://ff14angler.com/index.php?lang=cn&spot="+str(v)+"0000"
    html = requests.get(url=url).text
    ff=pq(html)
    # print(ff)
    ff_mapname = ''.join(re.findall(r'selected="selected">(.*?)</option>',ff.html()))
    ff_items=ff('table[class=list]').items()
    # print(ff_mapname)
    for i in ff_items:
        i=i.html()
        i=i.split(r'<tr><td class="area"')
        for ii in i:
            area=''.join(re.findall(r' colspan="4">(.*?)</td></tr>&#13;',ii))
            all=re.findall(r'<tr><td><a href="/spot/(.*?)">(.*?)</a></td>(.*?)<td class="text-right">.*?<img src="/img/i_spot(.*?)\.png" class="icon" title="地图"/></a></td></tr>&#13;',ii)
            # print(ff_mapname,area,all)
            for a in all:

                # print(a[3])
                thr=re.sub(r'<[^>]+>',"",a[2],re.S)
                thr=thr.split('　')
                areaname=a[1]
                if areaname=="Unspoiled teeming waters":
                    areaname="未知的鱼影"
                elif areaname=="North Isle of Endless Summer":
                    areaname="永夏岛北"
                elif areaname=="Northwest Bronze Lake":
                    areaname="石绿湖西北岸"
                if "".join(thr)!='' and "".join(a)!='' and a[3]=='1':
                    # print(ff_mapname,area,a[0],a[1],thr[0],thr[1])
                    sql.append("INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+areaname+"', '"+thr[1]+"', '"+thr[0]+"', '"+ff_mapname+"');")
                elif "".join(thr)!='' and "".join(a)!='' and a[3]=='2':
                    sql.append("INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+areaname+"', '"+thr[1]+"', '"+thr[0]+"', '"+ff_mapname+"');")
                elif "".join(thr)!='' and "".join(a)!='' and a[3]=='4':
                    sql.append("INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+areaname+"', '插鱼场', '"+thr[0]+"', '"+ff_mapname+"');")
                elif "".join(thr)!='' and "".join(a)!='' and a[3]=='5':
                    sql.append("INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+areaname+"', '"+thr[1]+"', '"+thr[0]+"', '"+ff_mapname+"');")
                else:
                    sql.append("INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+areaname+"', '', '', '"+ff_mapname+"');")

fishinfo.connecttomysql('DELETE FROM `ff_fisharea`')
fishinfo.connecttomysql(sql)



# INSERT INTO `ff_fisharea` (`area_id`, `big_map_name`, `area_name`, `is_eye`, `level`, `map_name`) VALUES ('"+a[0]+"', '"+area+"', '"+a[1]+"', '"+thr[1]+"', '"+thr[0]+"', '"+ff_mapname+"');
