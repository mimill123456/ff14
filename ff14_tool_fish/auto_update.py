#用于自动更新手动更新数据
import ff14_tool_fish.fishinfo as fishinfo

# 固定鱼名更新5.2鱼王
upsql = ["UPDATE `ff_fish` SET `fish_name`='不朽巨鱼' WHERE (`fish_id`='3193')",
         "UPDATE `ff_fish` SET `fish_name`='白色隆索' WHERE (`fish_id`='3194')",
         "UPDATE `ff_fish` SET `fish_name`='仙子彩虹鳉' WHERE (`fish_id`='3196')",
         "UPDATE `ff_fish` SET `fish_name`='刺钉蜥蜴' WHERE (`fish_id`='3195')",
         "UPDATE `ff_fish` SET `fish_name`='黑色喷气乱流' WHERE (`fish_id`='3197')",
         "UPDATE `ff_fish` SET `fish_name`='鳍人叹息' WHERE (`fish_id`='3198')"]
fishinfo.connecttomysql(upsql)