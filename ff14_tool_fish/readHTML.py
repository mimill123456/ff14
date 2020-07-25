import os
import ff14_tool_fish.fishinfo_fivepointtwo as fishinfo_fivepointtwo
import ff14_tool_fish.fishinfo as  fishinfo
import ff14_tool_fish.ff_area_fish as area_fish
# testid="418.html"
#
# fishinfo.fishinfo(testid)
# exit()
#######鱼数据更新1
file_names = os.listdir("F:/htmls/fish/")
sqls=[]
for file in  file_names:
    filename = "F:/htmls/fish/" + file
    sql = fishinfo_fivepointtwo.fishinfo_fivepointtwo(filename)
    sqls.append(sql)
# fishinfo.connecttomysql(sqls)

#######鱼数据更新2
# file_names = os.listdir("F:/htmls/fish_area/")
# sqls=[]
# for file in  file_names:
#     filename = "F:/htmls/fish_area/" + file
#     area_fish.upfishinfo(filename)


#######测试########
# select ="SELECT a.fish_id,a.fish_name,a.weather,a.time,c.fish_area_name,b.baitname,b.probability,b.is_small_to_big FROM ff_fish a LEFT JOIN ff_fish_area c ON a.`where`=c.fish_area_id  LEFT JOIN ff_bait_fish b ON a.fish_id=b.fishid "
# js=fishinfo.testMysql2(select)
# fishinfo.write_to_file("F:/htmls/json1.txt", str(js))
