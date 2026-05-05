from itertools import combinations
from random import uniform
from collections import Counter

from resic import TrojuhelnikovyResic, State
from runner import Runner
from pravidla import rs
from ban import ban
from formular import Formular


#test konzistence pravidel
resic = TrojuhelnikovyResic(rs, print_error=False)
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
    "S" : "S"
}
)
statistiky = Counter()

for trojice in combinations(formular.polozky, 3):

    for i in range(10):                 #počet pokusů
        resic = TrojuhelnikovyResic(rs, print_error=False)
        runner = Runner(resic)
        
        for pole in trojice:
            resic.set(pole["promena"], pole["pozice"], uniform(20, 70))
        
        #spuštění výpočtu
        runner.run(ban)

        statistiky[runner.stav] += 1
        
        if runner.stav == State.Unsolved:
            print("Chyba:")
            print(resic.promene)
            print(*(pole["nazev"] for pole in trojice), sep=", ")
            raise AssertionError("Trojúhelník se nepodařilo vyřešit.")

        for res in runner.vysledky:
            res.test()

        if runner.stav != State.Failure:
            break
    else:
        print("Varování:")
        print(*(pole["nazev"] for pole in trojice), sep=", ")
        print("Nepodařilo se najít existující trojúhelník.")

print(statistiky)
print("✅")