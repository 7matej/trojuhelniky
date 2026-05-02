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


#kosinová věta
@rs.rule("strana", "strana", 1, "strana", 2, "uhel", 0)
def kosinova_veta1(b, c, alfa):
    return sqrt(b**2 + c**2 - 2*b*c*cos(alfa))

@rs.rule("uhel", "strana", 0, "strana", 1, "strana", 2)
def kosinova_veta2(a, b, c):
    return acos((b**2 + c**2 - a**2)/(2*b*c))


#sinová věta
@rs.rule("strana", "uhel", 0, "2r", 0)
def sinova_veta1(alfa, d):
    return sin(alfa) * d

@rs.rule("uhel", "strana", 0, "2r", 0)
def sinova_veta2(a, d):
    alfa = asin(a/d)
    return alfa, (180 - alfa) % 360

@rs.rule("2r", "strana", 0, "uhel", 0)
def sinova_veta3(a, alfa):
    return a / sin(alfa)







rs.promene["uhel"][0] = 55
rs.promene["strana"][0] = 6.1
rs.promene["strana"][1] = 7.2

runner.run()

print("*************************************")
print("*************************************")
for resic in runner.resice:
    print("*************************************")
    pprint(resic.promene)
