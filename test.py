from itertools import combinations
from random import uniform
from collections import Counter

from resic import TrojuhelnikovyResic, State
from runner import Runner
from pravidla import rs
from ban import ban
from formular import Formular


#test konzistence pravidel
resic = TrojuhelnikovyResic(rs)
resic.set("strana", 0, 8)
resic.set("strana", 1, 9)
resic.set("strana", 2, 12)

runner = Runner(resic)
runner.run()

assert(runner.stav == State.Success)

for resic in runner.vysledky:
    resic.test()


#test úplnosti pravidel
formular = Formular(
{
    "strana" : ("a", "b", "c"),
    "uhel" : ("α", "β", "γ"),
    "r" : "r",
}
)
statistiky = Counter()

for trojice in combinations(formular.polozky, 3):
    
    resic = TrojuhelnikovyResic(rs)
    runner = Runner(resic)
    
    for pole in trojice:
        resic.set(pole["promena"], pole["pozice"], uniform(20, 70))
    
    runner.run(ban)

    statistiky[runner.stav] += 1
    if runner.stav == State.Unsolved:
        print("Chyba:")
        for pole in trojice:
            print(pole["nazev"])
        raise AssertionError

    for res in runner.vysledky:
        res.test()

print(statistiky)
print("✅")