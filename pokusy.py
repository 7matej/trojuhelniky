from mmath import *

def f(x):
    return x**2 - 3*x + 2

print(separuj_koreny(0, 2, f))
print(puleniintervalu(f, 0, 1.2))
print(f(0), f(2))
from pravidla import problemaricky_pripad

print(problemaricky_pripad(6.0001446811589165, 2*35.99913193397863 / 9.0, 2*35.99913193397863 / 12.0))