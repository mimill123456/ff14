from pyquery import PyQuery as pq
import re
import os
import ff14_tool_fish.fishinfo as fishinfo
file_names = os.listdir("F:/htmls/fish_area")

for file in file_names:
    print(file)
    filename="F:/htmls/fish_area/"+file
    file = file.replace(".html", "")
    # print(file)
    file_object = open(filename, 'r', encoding='utf-8')
    html =file_object.read()
    ff1 = pq(html)
    sel1 = ff1('form[name=spot_delete]').items()
    for p in sel1:
        a = p.find('td').items()
        for q in a:
            if q.html()!=None:
                id1 = re.findall(r'<a href="/fish/([0-9]*)">', q.html())
                if len(id1) == 0:
                    continue
                sql = "INSERT INTO `ff_area_fish` (`area_id`, `fish_id`) VALUES ('" + file+ "', '" + ''.join(id1) + "')"
                fishinfo.connecttomysql(sql)
                print(sql)
