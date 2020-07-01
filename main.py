from wowspy import Wows
from ships_id import Ship_id_2_name,Players_ships
from tools import time_translate,get_players_id
import os

def example():
    api_key = 'c6b7891e4dad607e07c8288046621bf2'
    my_api = Wows(api_key)

    # We will search for a player and then get its stats in this example
    player_name = 'die_ehre'

    # Api response from Wargaming
    # We only want one result, thus it's specified limit
    player_id_response = my_api.players(
        my_api.region.AS, player_name, fields='account_id', limit=1)
    print(player_id_response)

    # Get the player id from the api response
    player_id = player_id_response['data'][0]['account_id']

    # Now we will use this id to search for the player's stats
    # We only want the pvp stats here, it's specified in fields param
    player_stats_response = my_api.player_personal_data(
        my_api.region.AS, player_id, fields='statistics.pvp')
    print(player_stats_response)


def do(player_id):
    wows = Wows()
    id=str(player_id)

    #请求玩家的个人数据
    player_stats_response = wows.player_personal_data(
        wows.region.AS, player_id)
#    print(player_stats_response)

    data = player_stats_response['data'][id]

    print('\n')
    print('最后的战斗：', time_translate(data['last_battle_time']))
    print('注册日期：', time_translate(data['created_at']))
    print('等级：', data['leveling_tier'], '\n','------------------------------------------','\n')
    statistics_pvp = data['statistics']['pvp']
    print('PvP战斗场数：', statistics_pvp['battles'])
    print('PvP胜利：', statistics_pvp['wins'])
    print('PvP失败：', statistics_pvp['losses'])
    print('PvP胜率：%.2f' % (statistics_pvp['wins'] * 100 / statistics_pvp['battles']), '%')
    print('PvP存活：', statistics_pvp['survived_battles'])
    print('PvP存活率：%.2f' % (statistics_pvp['survived_battles'] * 100 / statistics_pvp['battles']), '%')
    print('PvP主炮命中率：%.2f' % (statistics_pvp['main_battery']['hits'] * 100 / statistics_pvp['main_battery']['shots']),
          '%')
    print('PvP总击杀：', statistics_pvp['frags'])
    print('PvP总侦测数：', statistics_pvp['ships_spotted'])
    print('PvP总伤害：', statistics_pvp['damage_dealt'])
    print('PvP总飞机击落：', statistics_pvp['planes_killed'])
    print('PvP最大伤害：', statistics_pvp['max_damage_dealt'])
    print('PvP最大经验：', statistics_pvp['max_xp'])
    print('PvP最多击杀：', statistics_pvp['max_frags_battle'])
    print('PvP最大飞机击落：', statistics_pvp['max_planes_killed'])


if __name__ == '__main__':
    try:
        print('\n----------WoWSinfo 预览版----------\n')
        ship_id_2_name=Ship_id_2_name()       #实例化船id与船名转化模块
        players_ships=Players_ships()    #实例化显示玩家的所有玩过的船模块
        while 1:
            name_input=str(input('输入玩家id(建议复制粘贴，不区分大小写)：'))
            player_id=get_players_id(name_input)
            if not player_id:
                print('无法找到此玩家')
            else:
                break
        player_id=int(player_id)

        do(player_id)
        input('\n按回车键继续查询单船信息\n')
        while 1:
            i = os.system("cls")
            players_ships.list_of_my_ships(player_id=player_id)
            players_ships.print_all_my_ships(ship_id_2_name)
            players_ships.ships_details(player_id=player_id,ship_id=players_ships.xuhao_2_ship_id(ship_id_2_name),ships_list=ship_id_2_name)
            input('\n按回车键继续\n')
    except Exception as ERR:
        print('发生错误，错误提示为：',ERR)
        input()
