from resic import TrojuhelnikovyResic, State

class Runner:
    def __init__(self, resic : TrojuhelnikovyResic):
        self.resice = [resic]
        self.state = State.Unknown
        self.id = 1

    def spust_resic(self, resic : TrojuhelnikovyResic):
        resic.run(self, self.id)
        self.id += 1

    def run(self):
        self.spust_resic(self.resice[0])
        
        #odstranění chybných výsledků
        self.vysledky = [resic for resic in self.resice if resic.stav == State.Success]


    def duplicate(self, spoustec : TrojuhelnikovyResic, vysledek, poradi, moznosti : tuple):
        for moznost in moznosti[1:]:
            novy = spoustec.copy()
            novy.promene[vysledek][poradi] = moznost
            self.resice.append(novy)
            self.spust_resic(novy)

    