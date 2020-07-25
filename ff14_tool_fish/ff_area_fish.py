import ff14_tool_fish.fishinfo as fishinfo
from bs4 import BeautifulSoup
import json

spotid = "100151.html"

def upfishinfo(filename):
    # filename = "F:/htmls/fish_area/" + spotid
    html = fishinfo.readfile(filename)
    print(filename)
    bs = BeautifulSoup(html, features="lxml")
    ######轻重杆########
    # 6 7 8 轻杆
    # 9 10 重杆
    # 11 12 13 鱼王杆
    # tug=tree.xpath('//canvas[@class="tug_graph"]/@data-value')
    tug = bs.find("table","info_section").find('tbody').findAll('tr')
    upsqls = []
    for tr in tug :
        if tr:
            tug_time = ""
            tug2 = ""
            tugs = tr.find('canvas')
            fish_id = tr.find('a').get("href")
            fish_id = fish_id.replace("/fish/", '')
            leves = tr.find('td', 'text-right').findAll('img')
            upleve = ""
            for leve in leves:
                if leve.get('title') == '理符任务':
                    upleve = "可"
            if tugs:
                tugs=tugs.get("data-value")
                tug1 = json.loads(str(tugs))
                tug_time = ",".join(tug1.keys())
                tuglist = []
                tugset = set()
                for k in tug1.keys():
                    if tug1[k]>0.9:
                        tuglist.append(int(k))
                for kk in tuglist:
                    if kk<=8 and kk>=6:
                        tugset.add('轻杆')
                    elif kk<=10 and kk>=9:
                        tugset.add('重杆')
                    elif kk<=13 and kk>=11:
                        tugset.add('鱼王杆')
                tuglist=list(tugset)
                tug2=",".join(tuglist)
            if upleve=='' and tug_time == '' and tug2 == '':
                continue
            else:
                sql = "UPDATE `ff_fish` SET `leve`='"+upleve+"',`tug_time`='"+tug_time+"',`tug`='"+tug2+"' WHERE (`fish_id`='"+fish_id+"')"
                print(sql)
                upsqls.append(sql)
    fishinfo.connecttomysql(upsqls)
# filename = "F:/htmls/fish_area/" + spotid
# upfishinfo(filename)
