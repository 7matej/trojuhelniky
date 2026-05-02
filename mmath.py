import math as m

def sin(alpha):
    return m.sin(m.radians(alpha))

def cos(alpha):
    return m.cos(m.radians(alpha))

def asin(x):
    return m.degrees(m.asin(x)) % 360

def acos(x):
    return m.degrees(m.acos(x)) % 360

sqrt = m.sqrt