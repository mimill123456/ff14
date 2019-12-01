import re
import pymysql
from lxml import etree
import json
import MySQLdb
import MySQLdb.cursors  #使用字典返回数据内容需要额外引用该模块
from pathlib import Path

def write_to_file(filename, con):
    file_object = open(filename, 'w', encoding='utf-8')
    file_object.write(con)
    file_object.close()


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


def testMysql2(sql):
    db = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='ff14',
                         cursorclass=MySQLdb.cursors.DictCursor, charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    # rs = str(rs)
    rs = json.dumps(rs)
    rs = rs.encode('utf-8').decode('unicode_escape')
    # print(type(rs))
    # print(rs)
    # rs=list(rs)
    cursor.close()
    db.close()

    return rs


def connecttomysql(sql):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', database='ff14',
                           charset='utf8mb4')
    cur = conn.cursor()
    if isinstance(sql,list):
        for s in sql:
            # print(sql)
            cur.execute(s)

    if isinstance(sql,str):
        cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

def readfile(filename):
    file = open(filename, "r", encoding="utf-8")
    con = file.read()
    file.close()
    return con

def timearea(t):
    if len(t) != 0:
        for x, i in enumerate(t):
            # x是下表，i是值
            if x < len(t) - 1:
                if int(i) + 1 != int(t[x + 1]):
                    # print("不连续")
                    sum = t[x + 1] + '-' + i
                    return sum
        sum = t[0] + '-' + t[len(t) - 1]
        return sum
    # print("时间异常")
def fishinfo(fileid):
    print(fileid)
    # id = "11"
    filename = "F:/htmls/fish/" + fileid
    html = readfile(filename)

    # xpath解析
    tree = etree.HTML(html)

    # pat3='<td><label>(.*?)</label></td>.*?<a href="/bait/(.*?)">.*?</span>(.*?)</a>(.*?)</td>'
    # html2="".join(res1)
    # res2=re.findall(pat1,html2,re.S)

    # 鱼基本信息
    pat_lv = '<span class="ilevel">(.*?)<span class="patch"'
    lv_res = re.findall(pat_lv, html, re.S)
    version = tree.xpath('//table[@class="fish_info"]/tr[2]/td/span/span/@patch')
    id = tree.xpath('//table[@class="fish_info"]/tr[2]/td[2]/@fish')
    name = tree.xpath('//a[@class="shortcut"]/@value')
    collect = tree.xpath('//table[@class="fish_info"]/tr[2]/td/span/img/@title')
    msg = tree.xpath('//table[@class="fish_info"]/tr[3]/td/text()')
    msg2 = tree.xpath('//table[@class="fish_info"]/tr[5]/td/text()')
    id = "".join(id)
    # print('id:'+id)
    name = "".join(name)
    # print('name:'+name)
    version = "".join(version)
    # print("version:"+version)

    lv_res = "".join(lv_res)
    lv_res = lv_res.replace("　", "")
    # print('lv'+lv_res)
    collect = "".join(collect)
    # if collect=="收藏品":
    #     print("收藏品")
    # else:
    #     # print(collect)
    #     print("非收藏品")
    msg = "".join(msg)
    # print('msg'+msg)
    msg2 = "".join(msg2)
    msg2 = msg2.replace("""
""", "")
    msg2 = msg2.replace("	","")
    # print('msg2'+msg2)
    #########场所########
    eye = tree.xpath('//table[@class="info_section list"]/tbody/tr[2]/td[3]/a/img/@src')
    spot = tree.xpath('//table[@class="info_section list"]/tbody/tr[2]/td/a/@href')[0]

    if "".join(eye) == '/img/i_spot1.png':
        eye = "普通鱼场"
    elif "".join(eye) == '/img/i_spot2.png':
        eye = "鱼鹰之眼"
    elif "".join(eye) == '/img/i_spot4.png':
        eye = "普通叉鱼场"
    elif "".join(eye) == '/img/i_spot5.png':
        eye = "鱼影"
    # print('eyes'+eye)
    spot = spot.split("/")[2]
    # print(spot)
    #######"时区"#######
    timearea1 = tree.xpath(
        '//table[@class="info_section timezone"]/tbody/tr/td/div[@class="tz_bar"]/../label/text()')
    time = ''
    if len(timearea1) == 24:
        time = '无时间限制'
        # print('无时间限制')
    else:
        time = '有时限，有效时间为：' + timearea(timearea1)
        # print('有时限，有效时间为：')
        # print(timearea(timearea1))
    #######天气#######
    weather = tree.xpath('//table[@class="info_section chart_weather"]/tbody/tr/td/label/span/text()')
    weather = ",".join(weather)
    # print(weather)
    #######选饵#######

    pat2 = '<form action="" method="post" name="bait_delete">.*?<tbody>(.*?)</tbody>.*?</form>'
    res1 = re.findall(pat2, html, re.S)

    pat1 = '<td><label>(.*?)</label></td>.*?<img src="/img/icon/(.*?).png"></span>(.*?)</a>(.*?)</td>'
    pat3 = '<td><label>(.*?)</label></td>.*?<a href="/bait/(.*?)">.*?</span>(.*?)</a>(.*?)</td>'
    html2 = "".join(res1)
    res2 = re.findall(pat1, html2, re.S)
    res3 = re.findall(pat3, html2, re.S)
    upsqls=[]
    fish_bait=[]

    if res3:
        for x in res3:
            fb = f_b()
            fb.bid = x[1]
            fb.bname = re.sub(r'<[^>]+>', "", x[2], re.S)
            fb.fid = id
            fb.fname = name
            fb.gl = x[0]
            if x[3]:
                bei_smalltobig=x[3]+"by"+re.sub(r'<[^>]+>',"",x[2],re.S)
                updatesql="UPDATE `ff_fish` SET `is_small_to_big`='"+x[3]+"' WHERE (`fish_id`='"+x[1]+"');"
                upsqls.append(updatesql)
                fb.stob=x[3]
            # print(fb)
            sql2 = "INSERT INTO `ff_bait_fish` (`fishid`, `fishname`, `baitid`, `baitname`, `probability`, `is_small_to_big`) VALUES ('"+fb.fid+"', '"+fb.fname+"', '"+fb.bid+"', '"+fb.bname+"', '"+fb.gl+"', '"+fb.stob+"');"
            fish_bait.append(sql2)
            print("起钓概率:",x[0],"鱼饵id:",x[1],"鱼饵:",re.sub(r'<[^>]+>',"",x[2],re.S),"是否以小钓大:",x[3])
    else:
        for x in res2:
            fb = f_b()
            fb.bname = re.sub(r'<[^>]+>', "", x[2], re.S)
            fb.fid = id
            fb.fname = name
            fb.gl = x[0]
            print(fb)
            sql2 = "INSERT INTO `ff_bait_fish` (`fishid`, `fishname`, `baitid`, `baitname`, `probability`, `is_small_to_big`) VALUES ('" + fb.fid + "', '" + fb.fname + "', '" + fb.bid + "', '" + fb.bname + "', '" + fb.gl + "', '" + fb.stob + "');"
            fish_bait.append(sql2)
            # print("起钓概率:",x[0],"鱼叉:",re.sub(r'<[^>]+>',"",x[2],re.S),"是否以小钓大:",x[3])

    ########用途######
    pat21='<h3 id="receipe">.*?<table class="list">(.*)</a></td></tr>'
    res21=re.findall(pat21,html,re.S)

    pat22='</td><td><img src="/img/i_relavant(.*?).png"'
    html21="".join(res21)
    res22=re.findall(pat22,html21,re.S)

    set1=set(res22)
    # res22="".join(res21)
    use=[]
    for us in  set1:
        if us=="008":
            use.append('食材')
        elif us=="007":
            use.append('炼金')
    use="".join(use)
    sql = "INSERT INTO `ff_fish` (`fish_id`, `fish_name`, `msg`, `msg2`, `is_small_to_big`, `IL`, `use`, `where`, `version`, `weather`,`collect`,`time`) VALUES ('" + id + "', '" + name + "', \"" + msg + "\", \"" + msg2 + "\", '', '" + lv_res + "', '"+use+"', '" + spot + "', '" + version + "', '" + weather + "','" + collect + "','" + time + "');"
    # connecttomysql(sql) #插入除以小钓大以外的数据
    # connecttomysql(upsqls) #更新以小钓大数据
    connecttomysql(fish_bait) #更新鱼与鱼饵关系
    return sql


# bait = tree.xpath('//form[@name="bait_delete"]/table/tbody/tr/td[2]/a/text()|//form[@name="bait_delete"]/table/tbody/tr/td[2]/text()')
# stob = tree.xpath('//form[@name="bait_delete"]/table/tbody/tr//a/text()')
# print(bait)
# print(stob)
# 所属渔场信息
