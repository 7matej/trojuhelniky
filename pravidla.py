from rule import Rule
from mmath import *
from pprint import pprint

promene = set((
    "strana",    #strana
    "uhel",    #úhel
    "r",    #poloměr kružnice opsané
    "S",    #obsah
))
rs = Rule(promene)


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

rs.cond("S", 0)
def podm5(S):
    return S > 0



#součet úhlů v trojúhelníku
@rs.rule("uhel", "uhel", 1, "uhel", 2)
def stoosumdesat(alfa, beta):
    return 180 - alfa - beta



#symetrické veličiny
@rs.rule("r", "r", 1)
def r(r):
    return r
@rs.rule("S", "S", 1)
def S(S):
    return S



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

@rs.rule("r", "strana", 0, "uhel", 0)
def sinova_veta2(a, alfa):
    return (a / sin(alfa))/2


#obsah
@rs.rule("S", "strana", 0, "uhel", 1, "strana", 2)
def obsah1(a, beta, c):
    return 1/2 * a*c * sin(beta)

@rs.rule("strana", "S", 0, "strana", 1, "uhel", 2)
def obsah2(S, b, gama):
    return 2*S / (b * sin(gama))


@rs.rule("strana", "S", 1, "uhel", 1, "strana", 1, "r", 1)
def SAlfaA(S, alfa, a, r):
    
    l = 4*r*S/a                 #b*c
    k = a**2 + 2*l*cos(alfa)    #b**2 + c**2

    z1, z2 = sqrt(k + 2*l), sqrt(k - 2*l)
    
    return (z1 + z2)/2, (z1 - z2)/2


@rs.rule("strana", "S", 0, "uhel", 0, "uhel", 1, "uhel", 2)
def podobnost(S, alfa, beta, gama):
    a0 = 10

    r0 = sinova_veta2(a0, alfa)
    b0 = sinova_veta1(beta, r0)
    S0 = obsah1(a0, gama, b0)

    return a0 * sqrt(S / S0)



#nejednoznačná pravidla - musí být na konci, jinak působí chyby!
@rs.rule("uhel", "strana", 0, "r", 0)
def sinova_veta3(a, r):
    return asin(a/(2*r))

@rs.rule("uhel", "S", 0, "strana", 1, "strana", 2)
def obsah3(S, b, c):
    return asin(2*S / (b * c))


#if __name__ == "__main__":
#    from runner import Runner
#
#    #rs.promene["uhel"][0] = 55
#    #rs.promene["strana"][0] = 6.1
#    #rs.promene["strana"][1] = 7.2
#
#    #rs.promene["strana"][0] = 4.3
#    #rs.promene["strana"][1] = 3.1
#    #rs.promene["uhel"][2] = 57 + 31/60
#
#    #rs.promene["strana"] = [4, 5, 3]
#
#    x = TrojuhelnikovyResic()
#    print(x.pravidla)
#    runner = Runner(x)
#
#    x.promene["strana"][0] = 6.1
#    x.promene["strana"][1] = 7.1
#    x.promene["uhel"][0] = 30
#
#    runner.run()
#
#    print("*************************************")
#    for resic in runner.vysledky:
#        pprint(resic.promene)
#    print("*************************************")
