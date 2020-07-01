# initialization意为初始化

from requests import get
from wowspy import Wows


def initialization():
    get('https://api.wows-numbers.com/personal/rating/expected/json/')
    pass
