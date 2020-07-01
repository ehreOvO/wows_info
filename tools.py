import time
from wowspy import Wows
from requests import get


def time_translate(time_stamp: int) -> str:     # 时间戳转时间
    time_array = time.localtime(time_stamp)
    result_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return result_time


def get_players_id(player_name: str):
    wows = Wows()
    player_id_response = wows.players(
        wows.region.AS, player_name, fields='account_id', limit=1)

    try:
        player_id = player_id_response['data'][0]['account_id']
    except IndexError:
        return None
    else:
        return str(player_id)


def initialization():
    try:
        f = open('temp_ava.temp', mode='r', encoding='utf-8')
    except FileNotFoundError:
        print('ava数据文件不存在，正在重新获取！')
        initialization_ava()
    except PermissionError:
        print('权限不足，奇怪的错误增加了！')
    else:
        print('ava文件已存在')

    try:
        f = open('temp_list.temp', mode='r', encoding='utf-8')
    except FileNotFoundError:
        print('list数据文件不存在，正在重新获取！')
        initialization_list()
    except PermissionError:
        print('权限不足，奇怪的错误增加了！')
    else:
        print('list文件已存在')


def initialization_ava():
    with open('temp_ava.temp', mode='w+', encoding='utf-8') as f:
        f.seek(0)
        var = str(get('https://api.wows-numbers.com/personal/rating/expected/json/').json())
        f.write(var)
        f.seek(0)
        return


def initialization_list():
    wows = Wows()
    list_total = {}

    print('正在下载船只名单..第 %d 页' % 1)
    list_temp = wows.warships(region=wows.region.AS, language='zh-cn', fields='name', page_no=1)
    list_total.update(list_temp['data'])
    for page in range(list_temp['meta']['page_total'] - 1):   # api中船列表每页做多打印100条，目前共5页
        print('正在下载船只名单..第 %d 页' % (page + 1))
        list_temp = wows.warships(region=wows.region.AS, language='zh-cn', fields='name', page_no=page + 2)
        list_total.update(list_temp['data'])
    print('正在下载船只名单..日本船')
    list_total.update(
        wows.warships(region=wows.region.AS, language='ja', fields='name', nation='japan')['data'])  # 把日本的船名字换成日语的
    print('正在下载船只名单..毛子船')
    list_total.update(
        wows.warships(region=wows.region.AS, language='en', fields='name', nation='ussr')['data'])  # 把日本的船名字换成日语的
    list_total['3751753552']['name'] = '让巴尔'

    with open('temp_list.temp', mode='w+', encoding='utf-8') as f:
        f.seek(0)
        var = str(list_total)
        f.write(var)
        f.seek(0)
        return


def ship_pr(ship_id: str, actualDmg: int, actualWins: int, actualFrags: int) -> int:
    with open('temp_ava.temp', mode='r', encoding='utf-8') as f:
        data = eval(f.read())['data']
        expectedDmg = data[str(ship_id)]['average_damage_dealt']
        expectedWins = data[str(ship_id)]['win_rate']
        expectedFrags = data[str(ship_id)]['average_frags']

    rDmg = actualDmg / expectedDmg
    rWins = actualWins / expectedWins
    rFrags = actualFrags / expectedFrags
    nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
    nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
    nWins = max(0, (rWins - 0.7) / (1 - 0.7))
    PR = 700 * nDmg + 300 * nFrags + 150 * nWins

    return PR


def _player_pr(player_id: int):
    wows = Wows()
    str_id = str(player_id)
    player_stats_response = wows.player_personal_data(region=wows.region.AS, account_id=player_id)
    data = player_stats_response['data'][str_id]
    statistics_pvp = data['statistics']['pvp']
    expect_total_damage = 0
    expect_total_wins = 0
    expect_total_frags = 0

    with open('temp_ava.temp', mode='r', encoding='utf-8') as f:
        expect_data = eval(f.read())['data']
    battle_times_per_ship = wows.statistics_of_players_ships(
        region=wows.region.AS,
        account_id=player_id,
        fields='ship_id,pvp')
    battle_times_per_ship = battle_times_per_ship['data'][str(player_id)]       # -> list

    for each_ship in range(len(battle_times_per_ship)):     # 循环玩家所有的船，取出详细信息用以累加
        expect_total_damage += expect_data[str(battle_times_per_ship[each_ship]['ship_id'])]['average_damage_dealt'] * battle_times_per_ship[each_ship]['pvp']['battles']
        expect_total_frags += expect_data[str(battle_times_per_ship[each_ship]['ship_id'])]['average_frags'] * battle_times_per_ship[each_ship]['pvp']['battles']
        expect_total_wins += expect_data[str(battle_times_per_ship[each_ship]['ship_id'])]['win_rate'] * battle_times_per_ship[each_ship]['pvp']['battles'] / 100

    total_damage = statistics_pvp['damage_dealt']
    total_wins = statistics_pvp['wins']
    total_frags = statistics_pvp['frags']

    rDmg = total_damage / expect_total_damage
    rFrags = total_frags / expect_total_frags
    rWins = total_wins / expect_total_wins

    nDmg = max(0, (rDmg - 0.4) / (1 - 0.4))
    nFrags = max(0, (rFrags - 0.1) / (1 - 0.1))
    nWins = max(0, (rWins - 0.7) / (1 - 0.7))

    PR = 700 * nDmg + 300 * nFrags + 150 * nWins
    return PR


def color(pr: int):
    """

     Skill	            Range
0    Bad	            0 - 750
1    Below Average	    750 - 1100
2    Average	        1100 - 1350
3    Good	            1350 - 1550
4    Very Good	        1550 - 1750
5    Great	            1750 - 2100
6    Unicum	            2100 - 2450
7    Super Unicum	    2450 - 9999

    """

    if 0 <= pr < 750:
        t = 0
        print('还需努力 +',750-pr)
    elif pr < 1100:
        t = 1
        print('低于平均 +',1100-pr)

    elif pr < 1350:
        t = 2
        print('平均水平 +',1350-pr)

    elif pr < 1550:
        t = 3
        print('好 +',1550-pr)

    elif pr < 1750:
        t = 4
        print('很好 +',1750-pr)

    elif pr < 2100:
        t = 5
        print('非常好 +',2100-pr)

    elif pr < 2450:
        t = 6
        print('大佬平均 +',2450-pr)

    elif pr < 9999:
        t = 7
        print('神佬平均 +', pr-2450)

    else:
        t = 8
        print('PR超出范围了！奇怪的错误增加了')

    return t


if __name__ == '__main__':
    while 1:
        print(color(int(input('value:'))))
