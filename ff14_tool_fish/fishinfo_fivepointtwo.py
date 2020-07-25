import re
from bs4 import BeautifulSoup

import ff14_tool_fish.fishinfo as fishinfo

class f_b:
    fid=""
    fname=""
    bid=""
    bname=""
    gl=""
    stob=""
    def __init__(self):
        pass
    def __repr__(self):
        return "fid:"+self.fid+" fname:"+self.fname+" bid:"+self.bid+" bname:"+self.bname+" gl:"+self.gl+" stob:"+self.stob

fileid = "4"+".html"

def fishinfo_fivepointtwo(filename):
    # filename = "F:/htmls/fish/" + fileid
    html = fishinfo.readfile(filename)
    print(filename)
    bs = BeautifulSoup(html,features="lxml")

    headinfo = bs.find('table',class_="fish_info")

    fishname = headinfo.find('span',class_="name").get_text()

    fishid = headinfo.find('span',class_="toggle_timetable").get("data-fish")

    msg = headinfo.find('td',colspan="3").get_text()
    msg = msg.replace('\n','').replace('\t','')

    msg2 = headinfo.find('td',colspan="4")
    if msg2:
        msg2 = msg2.get_text()
    else:
        msg2 = ""
    il = re.findall('<span class="ilevel">(.*?)<span class="patch"',str(headinfo))
    il = il[0].replace("\u3000","")

    use = bs.find("h3",id="receipe")
    uses = []
    if use:
        use = use.fetchNextSiblings()[0]
        use = use.find_all('img',class_="icon")
        for u in use:
            # print(u.get('src'))
            if u.get('src') == '/img/i_relavant007.png':
                uses.append("炼金")
            if u.get('src') == '/img/i_relavant008.png':
                uses.append("食材")
    use = ",".join(uses)

    version = headinfo.find('span',class_="patch").get('patch')

    weather = bs.find('tbody',class_="graph")
    weathers = []
    if weather:
        weather = weather.findAll('img')
        for wt in weather:
            weathers.append(wt.get('title'))
        weather = ",".join(weathers)
    else:
        weather = ""

    leve = bs.find('h3',id="leve")
    if leve:
        leve="可"
    else:
        leve=""

    time = bs.find('tr',class_="graph").findAll('td')
    times = []
    for td in time:
        if td.find('div'):
            # print(td.find('label').get_text())
            times.append(td.find('label').get_text())
    if len(times) == 24 :
        time = "无时间限制"
    else:
        time = '有时限，有效时间为：' + fishinfo.timearea(times)

    plus = headinfo.find('div',class_="fancy info_icon_area")
    gyotaku = plus.find('a')
    if gyotaku:
        gyotaku = gyotaku.get('data-text')
    else:
        gyotaku = ""

    doubleHooking = ""
    aquarium = ""
    if plus.find('span'):
        tmp = plus.find_all('span')
        for t in tmp:
            t1 = t.find('img').get('src')
            if t1 == "/img/double_hooking.png":
                doubleHooking = t.get('data-text')
            if t1.startswith('/img/aquarium'):
                aquarium = t.get('data-text')


    king = fishinfo.is_king(int(fishid))

    #######选饵#######

    pat2 = '<form action="" method="post" name="bait_delete">.*?<tbody>(.*?)</tbody>.*?</form>'
    res1 = re.findall(pat2, html, re.S)

    pat1 = '<td><label>(.*?)</label></td>.*?<img src="/img/icon/(.*?).png"></span>(.*?)</a>(.*?)</td>'
    pat3 = '<td><label>(.*?)</label></td>.*?<a href="/bait/(.*?)">.*?</span>(.*?)</a>(.*?)</td>'
    html2 = "".join(res1)
    res2 = re.findall(pat1, html2, re.S)
    res3 = re.findall(pat3, html2, re.S)
    upsqls = []
    fish_bait = []

    if res3:
        for x in res3:
            fb = f_b()
            fb.bid = x[1]
            fb.bname = re.sub(r'<[^>]+>', "", x[2], re.S)
            fb.fid = fishid
            fb.fname = fishname
            fb.gl = x[0]
            if x[3]:
                bei_smalltobig = x[3] + "by" + re.sub(r'<[^>]+>', "", x[2], re.S)
                updatesql = "UPDATE `ff_fish` SET `is_small_to_big`='" + x[3] + "' WHERE (`fish_id`='" + x[1] + "');"
                upsqls.append(updatesql)
                fb.stob = x[3]
            # print(fb)
            sql2 = "INSERT INTO `ff_bait_fish` (`fish_id`, `fishname`, `bait_id`, `baitname`, `probability`, `is_small_to_big`) VALUES ('" + fb.fid + "', \"" + fb.fname + "\", '" + fb.bid + "', \"" + fb.bname + "\", '" + fb.gl + "', '" + fb.stob + "');"
            fish_bait.append(sql2)
            # print("起钓概率:",x[0],"鱼饵id:",x[1],"鱼饵:",re.sub(r'<[^>]+>',"",x[2],re.S),"是否以小钓大:",x[3])
    else:
        for x in res2:
            fb = f_b()
            fb.bname = re.sub(r'<[^>]+>', "", x[2], re.S)
            fb.fid = fishid
            fb.fname = fishname
            fb.gl = x[0]
            # print(fb)
            sql2 = "INSERT INTO `ff_bait_fish` (`fish_id`, `fishname`, `bait_id`, `baitname`, `probability`, `is_small_to_big`) VALUES ('" + fb.fid + "', \"" + fb.fname + "\", '" + fb.bid + "', \"" + fb.bname + "\", '" + fb.gl + "', '" + fb.stob + "');"
            fish_bait.append(sql2)
            # print("起钓概率:",x[0],"鱼叉:",re.sub(r'<[^>]+>',"",x[2],re.S),"是否以小钓大:",x[3])

    fishinfo.connecttomysql(upsqls)         #更新以小钓大数据
    # fishinfo.connecttomysql(fish_bait)      #更新鱼与鱼饵关系
    # sql = "INSERT INTO `ff_fish` " \
    #       "(`fish_id`, `fish_name`, `msg`, `msg2`, `is_small_to_big`, `IL`, `use`, `version`, `weather`, `collect`, `leve`, `time`, `gyotaku`, `double_hooking`) VALUES" \
    #       " ('"+fishid+"', '"+fishname+"', '"+msg+"', '"+msg2+"', '', '"+il+"', '"+use+"', '"+version+"', '"+weather+"', '', '"+leve+"', '"+time+"', '"+gyotaku+"', '"+doubleHooking+"')"
    sql = "INSERT INTO `ff_fish` " \
          "(`fish_id`, `fish_name`, `msg`, `msg2`, `is_small_to_big`, `IL`, `use`, `version`, `weather`, `collect`, `leve`, `time`, `gyotaku`, `double_hooking` , `is_king` , `aquarium`) VALUES" \
          " ('%s', \"%s\", \"%s\", \"%s\", '', '%s', '%s', '%s', '%s', '', '%s', '%s', '%s', '%s', '%s', '%s')" %\
          (fishid,fishname,msg,msg2,il,use,version,weather,leve,time,gyotaku,doubleHooking,king,aquarium)
    return sql
    # fishinfo.connecttomysql(sql)


    # print(doubleHooking)
    # print('%r' % msg)

