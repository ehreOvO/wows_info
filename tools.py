import time
from wowspy import Wows

def time_translate(timeStamp:int)->str:
    #时间戳转时间
    timeArray = time.localtime(timeStamp)
    result_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return result_time

def get_players_id(player_name:str):
    wows = Wows()
    player_id_response = wows.players(
        wows.region.AS, player_name, fields='account_id', limit=1)

    try:
        player_id = player_id_response['data'][0]['account_id']
    except IndexError:
        return None
    else:
        id=str(player_id)
        return id
