from resic import TrojuhelnikovyResic, State
from runner import Runner
from pravidla import rs

resic = TrojuhelnikovyResic(rs)
resic.set("strana", 0, 8)
resic.set("strana", 1, 9)
resic.set("strana", 2, 12)

runner = Runner(resic)
runner.run()

assert(runner.stav == State.Success)

for resic in runner.vysledky:
    resic.test()