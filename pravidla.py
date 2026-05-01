from resic import TrojuhelnikovyResic
from runner import Runner
from mmath import *
from pprint import pprint

rs = TrojuhelnikovyResic(set((
    "strana",    #strana
    "uhel",    #úhel
    "2r"    #průměr kružnice opsané
)))
runner = Runner(rs)


#podmínky
@rs.cond("strana", 0)
def podm1(a):
    return a > 0

@rs.cond("uhel", 0)
def podm2(alfa):
    return 0 < alfa < 180

@rs.cond("strana", 0, "strana", 1, "strana", 2)
def trojuhelnikova_nerovnost(a, b, c):
    return a < b + c



#součet úhlů v trojúhelníku
@rs.rule("uhel", "uhel", 1, "uhel", 2)
def stoosumdesat(alfa, beta):
    return 180 - alfa - beta



#poloměr kruž. opsané
@rs.rule("2r", "2r", 1)
def r(r):
    return r


#sinová věta
@rs.rule("strana", "uhel", 0, "2r", 0)
def sinova_veta1(alfa, d):
    return sin(alfa) * d

@rs.rule("uhel", "strana", 0, "2r", 0)
def sinova_veta2(a, d):
    return asin(a/d)

@rs.rule("2r", "strana", 0, "uhel", 0)
def sinova_veta3(a, alfa):
    return a / sin(alfa)







rs.promene["strana"][2] = 3
rs.promene["uhel"][1] = 90
rs.promene["strana"][1] = 5

runner.run()

pprint(rs.promene)