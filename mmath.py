import math as m

def sin(alpha):
    return m.sin(m.radians(alpha))

def cos(alpha):
    return m.cos(m.radians(alpha))

def asin(x):
    r1 = m.degrees(m.asin(x)) % 360
    return r1, (180 - r1) % 360

def acos(x):
    return m.degrees(m.acos(x)) % 360

sqrt = m.sqrt


def puleniintervalu(f, min, max):
    #print("Puleni", min, max)
    d = 0.0000000000001        #přesnost

    while max-min > d:
        s=(max+min)/2
        if f(s)*f(min) <= 0:
            max=s
        elif f(s)*f(max) > 0:
            print("Řešení ztraceno !!!")
            return None
        else:
            min=s

    return (max + min)/2

def separuj_koreny(min, max, f):
    #print("Separace")
    n = 2**14         #rozdělí interval na 2**7 částí
    vysledky = []

    predchozic = min
    predchozif = f(min)
    for i in range(1, n+1):
        cislo = min + i*(max - min)/n
        
        fce = f(cislo)
        #print(fce)
        if fce * predchozif <= 0:
            vysledek = puleniintervalu(f, predchozic, cislo)
            if vysledek is not None:
                vysledky.append(vysledek)

        predchozic = cislo
        predchozif = fce

    return vysledky
