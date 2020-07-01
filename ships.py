from wowspy import Wows
from prettytable import PrettyTable
from tools import time_translate, ship_pr, color


def ship_id_2_name(ship_id: str):
    with open('temp_list.temp', mode='r', encoding='utf-8') as f:
        list_total = eval(f.read())
    try:
        ship_name = list_total[ship_id]['name']
        return ship_name
    except KeyError:
        print('ship_id没有查询到，ship_id=', ship_id)


def player_stats(player_id):
    wows = Wows()
    pt = PrettyTable()
    str_id = str(player_id)

    # 请求玩家的个人数据
    player_stats_response = wows.player_personal_data(region=wows.region.AS, account_id=player_id)
    data = player_stats_response['data'][str_id]
    statistics_pvp = data['statistics']['pvp']

    pt.field_names = ['账号id', str_id]
    pt.add_row(['最后的战斗', time_translate(data['last_battle_time'])])
    pt.add_row(['PvP场数', statistics_pvp['battles']])
    pt.add_row(['PvP胜利', statistics_pvp['wins']])
    pt.add_row(['PvP失败', statistics_pvp['losses']])
    try:  # 防止被除数为0的情况
        pt.add_row(['PVP胜率', str(round(statistics_pvp['wins'] / statistics_pvp['battles'] * 100, 2)) + '%'])
    except ZeroDivisionError:
        pt.add_row(['PVP胜率', 'NULL'])
    try:
        pt.add_row(['PVP场均伤害', int(round(statistics_pvp['damage_dealt'] / statistics_pvp['battles'], 0))])
    except ZeroDivisionError:
        pt.add_row(['PVP场均伤害', 'NULL'])
    try:
        pt.add_row(['PVP场均经验', int(round(statistics_pvp['xp'] / statistics_pvp['battles'], 0))])
    except ZeroDivisionError:
        pt.add_row(['PVP场均经验', 'NULL'])
    pt.add_row(['PvP存活', statistics_pvp['survived_battles']])
    try:
        pt.add_row(
            ['PvP存活率', str(round(statistics_pvp['survived_battles'] / statistics_pvp['battles'] * 100, 2)) + '%'])
    except ZeroDivisionError:
        pt.add_row(['PvP存活率', 'NULL'])
    try:
        pt.add_row(
            ['PVP主炮命中率', round(statistics_pvp['main_battery']['hits'] / statistics_pvp['main_battery']['shots'], 2)])
    except ZeroDivisionError:
        pt.add_row(['PVP主炮命中率', 'NULL'])
    pt.add_row(['PvP总击杀', statistics_pvp['frags']])
    pt.add_row(['PvP总侦测数', statistics_pvp['ships_spotted']])
    pt.add_row(['PvP总伤害', statistics_pvp['damage_dealt']])
    pt.add_row(['PvP总飞机击落', statistics_pvp['planes_killed']])
    pt.add_row(['PvP最大伤害', statistics_pvp['max_damage_dealt']])
    pt.add_row(['PvP最大经验', statistics_pvp['max_xp']])
    pt.add_row(['PvP最多击杀', statistics_pvp['max_frags_battle']])
    pt.add_row(['PvP最大飞机击落', statistics_pvp['max_planes_killed']])

    print(pt)


class PlayersShips:
    def __init__(self, player_id):
        wows = Wows()
        self.__player_ships_list = {}
        ships_list = wows.statistics_of_players_ships(region=wows.region.AS, account_id=player_id, fields='ship_id')
        self.__player_ships_list = ships_list['data'][str(player_id)]
        self.player_ships_list = self.__player_ships_list       # 用于被其他方法访问时使用


    def print_all_my_ships(self):
        pt = PrettyTable()
        pt.field_names = ['序号', '船名', 'ship_id']
        for i in range(len(self.__player_ships_list)):
            name = ship_id_2_name(str(self.__player_ships_list[i]['ship_id']))
            ship_id = self.__player_ships_list[i]['ship_id']
            pt.add_row([i + 1, name, ship_id])
        print(pt)
        return pt

    def xuhao_2_ship_id(self):
        while 1:
            try:
                xuhao_input = int(input('输入所选择的船序号：')) - 1
                print('选择的船是：', ship_id_2_name(str(self.__player_ships_list[xuhao_input]['ship_id'])))
            except IndexError:
                print('序号不存在！请重新输入：')
            except ValueError:
                print('序号不存在！请重新输入：')
            else:
                return self.__player_ships_list[xuhao_input]['ship_id']

    def ships_details(self, player_id: int, ship_id: int):
        wows = Wows()
        pt = PrettyTable()
        pt.field_names = ['项目', '值']
        ship_details = wows.statistics_of_players_ships(account_id=player_id, ship_id=ship_id, region=wows.region.AS)
        pvp = ship_details['data'][str(player_id)][0]['pvp']
        pt.add_row(['船名', ship_id_2_name(str(ship_id))])
        pt.add_row(['最后的战斗', time_translate(ship_details['data'][str(player_id)][0]['last_battle_time'])])
        pt.add_row(['PvP场数', pvp['battles']])
        pt.add_row(['PvP胜利', pvp['wins']])
        pt.add_row(['PvP失败', pvp['losses']])
        try:  # 防止被除数为0的情况
            pt.add_row(['PVP胜率', str(round(pvp['wins'] / pvp['battles'] * 100, 2)) + '%'])
        except ZeroDivisionError:
            pt.add_row(['PVP胜率', 'NULL'])
        try:
            pt.add_row(['PVP场均伤害', int(round(pvp['damage_dealt'] / pvp['battles'], 0))])
        except ZeroDivisionError:
            pt.add_row(['PVP场均伤害', 'NULL'])
        try:
            pt.add_row(['PVP场均击杀', str(round(pvp['frags'] / pvp['battles'], 2))])
        except ZeroDivisionError:
            pt.add_row(['PVP场均伤害', 'NULL'])
        try:
            pt.add_row(['PVP场均经验', int(round(pvp['xp'] / pvp['battles'], 0))])
        except ZeroDivisionError:
            pt.add_row(['PVP场均经验', 'NULL'])
        pt.add_row(['PvP存活', pvp['survived_battles']])
        try:
            pt.add_row(['PvP存活率', str(round(pvp['survived_battles'] / pvp['battles'] * 100, 2)) + '%'])
        except ZeroDivisionError:
            pt.add_row(['PvP存活率', 'NULL'])
        try:
            pt.add_row(['PVP主炮命中率', round(pvp['main_battery']['hits'] / pvp['main_battery']['shots'], 2)])
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

        print('PR:', end='')
        try:
            PR = ship_pr(
                ship_id=ship_id,
                actualDmg=pvp['damage_dealt'] / pvp['battles'],
                actualFrags=pvp['frags'] / pvp['battles'],
                actualWins=pvp['wins'] / pvp['battles']*100)
            PR = int(round(PR, 0))
        except:
            print('0')
        else:
            print(PR)
            color(PR)


if __name__ == '__main__':
    a = ship_id_2_name(str(3751753552))
    print(a)
    pass
