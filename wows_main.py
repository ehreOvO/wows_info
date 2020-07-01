import requests
import time


class Wows:

    def __init__(self,name:str):
        self.__application_id = 'c6b7891e4dad607e07c8288046621bf2'
        self.__region = 'asia'
        self.__blankurl = 'https://api.worldofwarships.{}/wows/{}/{}/?'
        self.__name=name


    def get_id(self)->int:
        last='application_id={}&search={}'
        last=last.format(self.__application_id,self.__name)
        result=requests.get(self.__blankurl.format(self.__region,'account','list')+last)
        result = result.json()

        account_id=result['data'][0]['account_id']
        self.__account_id=account_id
        return account_id

    def get_info(self)->dict:
        last='application_id={}&account_id={}'
        last=last.format(self.__application_id,self.__account_id)
        result=requests.get(self.__blankurl.format(self.__region,'account','info')+last)
        result=result.json()
        print(result)
        self.__result_info=result
        #print(result)
        return result



    def time_translate(self,timeStamp:int)->str:
        #时间戳转时间
        timeArray = time.localtime(timeStamp)
        result_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return result_time

    def print_info(self):
        id=str(self.__account_id)
        data=self.__result_info['data'][id]
        print('玩家昵称：',self.__name)
        print('最后战斗：',time_translate(data['last_battle_time']))
        print('注册日期：',time_translate(data['created_at']))
        print('等级：',data['leveling_tier'],'\n')
        statistics_pvp=data['statistics']['pvp']
        print('PvP战斗场数：',statistics_pvp['battles'])
        print('PvP胜利：',statistics_pvp['wins'])
        print('PvP失败：',statistics_pvp['losses'])
        print('PvP胜率：%.2f'%(statistics_pvp['wins']*100/statistics_pvp['battles']),'%')
        print('PvP存活：',statistics_pvp['survived_battles'])
        print('PvP存活率：%.2f'%(statistics_pvp['survived_battles']*100/statistics_pvp['battles']),'%')
        print('PvP主炮命中率：%.2f'%(statistics_pvp['main_battery']['hits']*100/statistics_pvp['main_battery']['shots']),'%')
        print('PvP总击杀：',statistics_pvp['frags'])
        print('PvP总侦测数：',statistics_pvp['ships_spotted'])
        print('PvP总伤害：',statistics_pvp['damage_dealt'])
        print('PvP总飞机击落：',statistics_pvp['planes_killed'])
        print('PvP最大伤害：',statistics_pvp['max_damage_dealt'])
        print('PvP最大经验：',statistics_pvp['max_xp'])
        print('PvP最多击杀：',statistics_pvp['max_frags_battle'])
        print('PvP最大飞机击落：',statistics_pvp['max_planes_killed'])





def time_translate(timeStamp:int)->str:
    #时间戳转时间
    timeArray = time.localtime(timeStamp)
    result_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return result_time

if __name__=='__main__':
    wows=Wows('die_ehre')
    wows.get_id()
    print(wows.get_info())
    wows.print_info()