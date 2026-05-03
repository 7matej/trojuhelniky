from resic import TrojuhelnikovyResic
from mmath import *
from pprint import pprint

rs = TrojuhelnikovyResic(set((
    "strana",    #strana
    "uhel",    #úhel
    "r"    #poloměr kružnice opsané
)))


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

rs.cond("r", 0)
def podm4(r):
    return r > 0



#součet úhlů v trojúhelníku
@rs.rule("uhel", "uhel", 1, "uhel", 2)
def stoosumdesat(alfa, beta):
    return 180 - alfa - beta



#poloměr kruž. opsané
@rs.rule("r", "r", 1)
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
@rs.rule("strana", "uhel", 0, "r", 0)
def sinova_veta1(alfa, r):
    return sin(alfa) * 2*r

@rs.rule("uhel", "strana", 0, "r", 0)
def sinova_veta2(a, r):
    alfa = asin(a/(2*r))
    return alfa, (180 - alfa) % 360

@rs.rule("r", "strana", 0, "uhel", 0)
def sinova_veta3(a, alfa):
    return (a / sin(alfa))/2





if __name__ == "__main__":
    from runner import Runner

    #rs.promene["uhel"][0] = 55
    #rs.promene["strana"][0] = 6.1
    #rs.promene["strana"][1] = 7.2

    #rs.promene["strana"][0] = 4.3
    #rs.promene["strana"][1] = 3.1
    #rs.promene["uhel"][2] = 57 + 31/60

    #rs.promene["strana"] = [4, 5, 3]

    x = TrojuhelnikovyResic()
    print(x.pravidla)
    runner = Runner(x)

    x.promene["strana"][0] = 6.1
    x.promene["strana"][1] = 7.1
    x.promene["uhel"][0] = 30

    runner.run()

    print("*************************************")
    for resic in runner.vysledky:
        pprint(resic.promene)
    print("*************************************")
