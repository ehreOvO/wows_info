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
        print('ava数据文件不存在，即将重新获取！')
        initialization_ava()
    except PermissionError:
        print('权限不足，奇怪的错误增加了！')
    else:
        print('ava文件已存在')

    try:
        f = open('temp_list.temp', mode='r', encoding='utf-8')
    except FileNotFoundError:
        print('list数据文件不存在，即将重新获取！')
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
    for page in range(5):   # api中船列表每页做多打印100条，目前共5页
                            # 不安全，后续修改！！！
        print('正在下载船只名单..第 %d 页' % (page + 1))
        list_temp = wows.warships(region=wows.region.AS, language='zh-cn', fields='name', page_no=page + 1)
        list_total.update(list_temp['data'])
    print('正在下载船只名单..日本船')
    list_total.update(
        wows.warships(region=wows.region.AS, language='ja', fields='name', nation='japan')['data'])  # 把日本的船名字换成日语的
    print('正在下载船只名单..毛子船')
    list_total.update(
        wows.warships(region=wows.region.AS, language='en', fields='name', nation='ussr')['data'])  # 把日本的船名字换成日语的

    with open('temp_list.temp', mode='w+', encoding='utf-8') as f:
        f.seek(0)
        var = str(list_total)
        f.write(var)
        f.seek(0)
        return


if __name__ == '__main__':
    pass
