from wowspy import Wows
from ships import PlayersShips, player_stats
from tools import time_translate, get_players_id, initialization
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


def run():
    print('\n----------WoWSinfo 预览版----------\n')
    initialization()
    # ship_id_2_name=Ship_id_2_name()       #实例化船id与船名转化模块
    players_ships = PlayersShips()  # 实例化显示玩家的所有玩过的船模块
    while 1:
        name_input = str(input('输入玩家id(建议复制粘贴，不区分大小写)：'))
        player_id = get_players_id(name_input)
        if not player_id:
            print('无法找到此玩家')
        else:
            break
    player_id = int(player_id)

    player_stats(player_id)
    input('\n按回车键继续查询单船信息\n')
    while 1:
        i = os.system("cls")
        players_ships.list_of_my_ships(player_id=player_id)
        players_ships.print_all_my_ships()
        players_ships.ships_details(player_id=player_id, ship_id=players_ships.xuhao_2_ship_id())
        input('\n按回车键继续\n')


if __name__ == '__main__':
    run()
