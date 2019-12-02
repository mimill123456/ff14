# import sys
# sys.path.append(r"F:\PycharmProjects\Utils")
import fishinfo
import json


sql="SELECT a.fish_id,a.fish_name,a.time,a.weather,b.area_name from ff_fish a LEFT JOIN ff_fisharea b ON a.`where`=b.area_id"
res=fishinfo.testMysql2(sql)
js=json.loads(res)
resx={}
for x in js:
    x["baits"]=[]
    x["areas"]=[]
    resx[x["fish_name"]]=x


sql1 ="SELECT a.fish_id,a.fish_name,a.time,a.weather,b.area_id,b.area_name,c.baitname,c.probability from ff_fish a LEFT JOIN ff_fisharea b ON a.`where`=b.area_id LEFT JOIN ff_bait_fish c ON a.fish_id=c.fish_id"

res1=fishinfo.testMysql2(sql1)
js1=json.loads(res1)
for y in js1:
    resj={}
    if y["fish_name"]==resx[y["fish_name"]]["fish_name"]:
        resj["baitname"]=y["baitname"]
        resj["probability"]=y["probability"]
        resx[y["fish_name"]]["baits"].append(resj)



sql2="SELECT a.*,c.fish_name FROM ff_fisharea a LEFT JOIN ff_area_fish b ON a.area_id=b.area_id LEFT JOIN ff_fish c ON b.fish_id=c.fish_id"
res2=fishinfo.testMysql2(sql2)
js2=json.loads(res2)
for f in js2:
    print(f["fish_name"])
    if f["fish_name"]:
        if f["fish_name"]==resx[f["fish_name"]]["fish_name"]:
            resx[f["fish_name"]]["areas"].append(f["area_name"])



world_map={}
big_big_mapkey=set()
big_map=set()
fishs={}
for z in js2:
    big_big_mapkey.add(z["map_name"])
    fishs[z["area_id"]] = set()

for zz in big_big_mapkey:
    world_map[zz]={}
    for z in js2:
        for fish in fishs.keys():
            if z["area_id"] == fish:
                if z["fish_name"]:
                    fishs[fish].add(z["fish_name"])
                else:
                    fishs[fish].add("不可思议！这里没有鱼！！！！")
        if z["map_name"]==zz:
            world_map[zz][z["big_map_name"]]={}

# print(fishs)
for world in world_map.keys():
    for big_map in  world_map[world].keys():
            for z in js2:
                if z["big_map_name"]==big_map:
                    world_map[world][big_map][z["area_id"]] = {}
                    world_map[world][big_map][z["area_id"]]["area_id"] = z["area_id"]
                    world_map[world][big_map][z["area_id"]]["area_name"] = z["area_name"]
                    world_map[world][big_map][z["area_id"]]["is_eye"] = z["is_eye"]
                    world_map[world][big_map][z["area_id"]]["level"] = z["level"]
                    world_map[world][big_map][z["area_id"]]["fishs"] = []
                    # world_map[world][big_map].append(area)
for world in world_map.keys():
    for big_map in  world_map[world].keys():
        for area in world_map[world][big_map].keys():
            world_map[world][big_map][area]["fishs"]=list(fishs[area])

# print(world_map)
resz={}
resz["fishinfo"]=resx
resz["areainfo"]=world_map
fishinfo.write_to_file("F:/htmls/json5.txt",str(resz))