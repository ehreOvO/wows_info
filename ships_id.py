from wowspy import Wows
from prettytable import PrettyTable
import tools

class Ship_id_2_name:
    list_total = {}
    def __init__(self):
        wows=Wows()
        for page in range(5):   #api中船列表每页做多打印100条，目前共5页
                                #不安全，后续修改！！！
            print('正在加载船只名单..第 %d 页' % (page+1))
            list_temp = wows.warships(region=wows.region.AS, language='zh-cn', fields='name', page_no=page+1)
            self.list_total.update(list_temp['data'])
        print('正在加载船只名单..日本船')
        self.list_total.update(wows.warships(region=wows.region.AS, language='ja', fields='name', nation='japan')['data'])      #把日本的船名字换成日语的
        print('正在加载船只名单..毛子船')
        self.list_total.update(wows.warships(region=wows.region.AS, language='en', fields='name', nation='ussr')['data'])      #把日本的船名字换成日语的

    def id_2_name(self,ship_id: str):
        try:
            ship_name=self.list_total[ship_id]['name']
            return ship_name
        except KeyError:
            print('ship_id没有查询到，ship_id=',ship_id)


class Players_ships:

    def list_of_my_ships(self, player_id: int) -> list:
        wows=Wows()
        ships_list=wows.statistics_of_players_ships(region=wows.region.AS,account_id=player_id,fields='ship_id')
        #print(ships_list)
        self.player_ships_list=ships_list['data'][str(player_id)]
        #print(self.player_ships_list.items())
        return self.player_ships_list

    def print_all_my_ships(self, ships_list) -> str:
        pt = PrettyTable()
        pt.field_names = ['序号', '船名', 'ship_id']
        for i in range(len(self.player_ships_list)):
            name = ships_list.id_2_name(str(self.player_ships_list[i]['ship_id']))
            ship_id=self.player_ships_list[i]['ship_id']
            #print(self.player_ships_list[i]['ship_id'])
            #print('%10s\t\t%d'%(name,id))
            pt.add_row([i+1, name, ship_id])
        print(pt)
        return pt

    def xuhao_2_ship_id(self, ships_list):
        xuhao = int(input('输入所选择的船序号：'))-1
        print('选择的船是：',ships_list.id_2_name(str(self.player_ships_list[xuhao]['ship_id'])))
        return self.player_ships_list[xuhao]['ship_id']

    def ships_details(self, player_id: int, ship_id: int, ships_list):
        wows = Wows()
        pt = PrettyTable()
        pt.field_names=['项目', '值']
        ship_details=wows.statistics_of_players_ships(account_id=player_id, ship_id=ship_id, region=wows.region.AS)
        pvp = ship_details['data'][str(player_id)][0]['pvp']
        pt.add_row(['船名', ships_list.id_2_name(str(ship_id))])
        pt.add_row(['最后的战斗', tools.time_translate(ship_details['data'][str(player_id)][0]['last_battle_time'])])
        pt.add_row(['PvP场数', pvp['battles']])
        pt.add_row(['PvP胜利', pvp['wins']])
        pt.add_row(['PvP失败', pvp['losses']])
        try:        # 防止被除数为0的情况
            pt.add_row(['PVP胜率', str(round(pvp['wins']/pvp['battles']*100, 2))+'%'])
        except ZeroDivisionError:
            pt.add_row(['PVP胜率', 'NULL'])
        try:
            pt.add_row(['PVP场均伤害', round(pvp['damage_dealt']/pvp['battles'], 0)])
        except ZeroDivisionError:
            pt.add_row(['PVP场均伤害', 'NULL'])
        try:
            pt.add_row(['PVP场均经验', round(pvp['xp']/pvp['battles'], 0)])
        except ZeroDivisionError:
            pt.add_row(['PVP场均经验', 'NULL'])
        pt.add_row(['PvP存活', pvp['survived_battles']])
        try:
            pt.add_row(['PvP存活率', str(round(pvp['survived_battles']/pvp['battles']*100, 2))+'%'])
        except ZeroDivisionError:
            pt.add_row(['PvP存活率', 'NULL'])
        try:
            pt.add_row(['PVP主炮命中率', round(pvp['main_battery']['hits']/pvp['main_battery']['shots'], 2)])
        except ZeroDivisionError:
            pt.add_row(['PVP主炮命中率', 'NULL'])
        pt.add_row(['PvP总击杀', pvp['frags']])
        pt.add_row(['PvP总侦测数', pvp['ships_spotted']])
        pt.add_row(['PvP总伤害', pvp['damage_dealt']])
        pt.add_row(['PvP总飞机击落', pvp['planes_killed']])
        pt.add_row(['PvP最大伤害', pvp['max_damage_dealt']])
        pt.add_row(['PvP最大经验', pvp['max_xp']])
        pt.add_row(['PvP最多击杀', pvp['max_frags_battle']])
        pt.add_row(['PvP最大飞机击落', pvp['max_planes_killed']])

        print(pt)


if __name__ == '__main__':
    ship_id = input('ship id')
    ship_id_2_name=Ship_id_2_name()

    print(ship_id_2_name.id_2_name(ship_id))