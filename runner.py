from resic import TrojuhelnikovyResic, State

class Runner:
    def __init__(self, resic : TrojuhelnikovyResic):
        self.resice = [resic]
        self.state = State.Unknown

    def run(self):
        self.resice[0].run(self)

    def duplicate(self, spoustec : TrojuhelnikovyResic, vysledek, poradi, moznosti : tuple):
        for moznost in moznosti[1:]:
            novy = spoustec.copy()
            novy.promene[vysledek][poradi] = moznost
            self.resice.append(novy)
            novy.run(self)