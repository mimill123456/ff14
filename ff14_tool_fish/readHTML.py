import os
import GitHub_ff14.fishinfo as fishinfo

testid="418.html"

fishinfo.fishinfo(testid)
exit()
file_names = os.listdir("F:/htmls/fish/")
sqls=[]
for file in  file_names:
    sql = fishinfo.fishinfo(file)
    sqls.append(sql)
fishinfo.connecttomysql(sqls)


#######测试########
# select ="SELECT a.fish_id,a.fish_name,a.weather,a.time,c.fish_area_name,b.baitname,b.probability,b.is_small_to_big FROM ff_fish a LEFT JOIN ff_fish_area c ON a.`where`=c.fish_area_id  LEFT JOIN ff_bait_fish b ON a.fish_id=b.fishid "
# js=fishinfo.testMysql2(select)
# fishinfo.write_to_file("F:/htmls/json1.txt", str(js))
