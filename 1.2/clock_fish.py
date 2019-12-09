import json
import fishinfo


file_object = open('F:/data.json', 'r', encoding='utf-8')
html = file_object.read()
html=json.loads(html)
sqls=[]
fish_names={}
for i in html['ITEMS']:

    items=html['ITEMS'][i]
    id=items['_id']
    name=items['name_en']
    fish_names[id]=name
    # print(fish_names)

weather_names={}
for w in html['WEATHER_TYPES']:
    weather_name=html['WEATHER_TYPES'][w]['name_en']
    weather_names[w]=weather_name

folklore_names={}
for f in html['FOLKLORE']:
    fname=html['FOLKLORE'][f]['name_en']
    folklore_names[f]=fname

for ii in html['FISH']:
    fish=html['FISH'][ii]
    fish_id=fish['_id']
    fish_name=fish_names[fish_id]  #
    pW=fish['previousWeatherSet']  #前置天气
    weather=fish['weatherSet']
    folklore=''
    if fish['folklore']:
        folklore=folklore_names[str(fish['folklore'])]
    collectable=fish['collectable']
    fishEyes=fish['fishEyes']
    hookset=fish['hookset']
    tug=fish['tug']
    best_catch_path=fish['bestCatchPath']
    ##############################
    bfish=[]
    for b in best_catch_path:
        bfish.append(fish_names[b])
    bfish=",".join(bfish)   #包装后的鱼饵
    pws=[]
    for ww in pW:
        if ww:
            pws.append(weather_names[str(ww)])
        else:
            pws.append('')
    pws=",".join(pws)  #包装后的前置天气
    ws=[]
    for www in weather:
        if www:
            ws.append(weather_names[str(www)])
        else:
            ws.append('')
    ws=",".join(ws)   #包装后的天气
    ###############################
    if tug=='light':
        tug='轻杆'
    elif tug=='medium':
        tug='重杆'
    elif tug=='heavy':
        tug='鱼王杆'
    else:
        tug=''
    ##############################
    if hookset=='Powerful':
        hookset='强力提钩'
    elif hookset=='Precision':
        hookset='精准提钩'
    else:
        hookset=''
    ###############################

    # print('id:',fish_id,'name:',fish_name,'前置天气:',pW,'天气:',weather,'传承录:',folklore,'收藏品:',collectable,'鱼眼技能:',fishEyes,'提钩技能:',hookset,'杆形:',tug)
    # print(weather_names)
    sql="INSERT INTO `clock_fish` (`fish_id`, `fish_name`, `tug`, `hookset`, `collect`, `fish_eye_skill`, `folklore`, `best_catch_path`, `previous_weather`, `weather`) VALUES ('"+str(fish_id)+"', \""+str(fish_name)+"\", '"+str(tug)+"', '"+str(hookset)+"', '"+str(collectable)+"', '"+str(fishEyes)+"', '"+str(folklore)+"', '"+str(bfish)+"', '"+str(pws)+"', '"+str(ws)+"');"

    sql2=''
    if tug!='':
        sql2="UPDATE `ff_fish` SET `tug`='"+str(tug)+"',`folklore`='"+str(folklore)+"', `hookset`='"+str(hookset)+"', `pweather`='"+str(pws)+"', `fish_eyes_skill`='"+str(fishEyes)+"' WHERE (`fish_name`=\""+str(fish_name)+"\")"
    else:
        sql2 = "UPDATE `ff_fish` SET `folklore`='" + str(folklore) + "', `hookset`='" + str(
            hookset) + "', `pweather`='" + str(pws) + "', `fish_eyes_skill`='" + str(
            fishEyes) + "' WHERE (`fish_name`=\"" + str(fish_name) + "\")"
    sqls.append(sql2)
    # print(sql)
fishinfo.connecttomysql(sqls)

'''UPDATE `ff_fish` SET `folklore`='1', `hookset`='1', `pweather`='1', `fish_eyes_skill`='1' WHERE (`fish_name`='1')'''

