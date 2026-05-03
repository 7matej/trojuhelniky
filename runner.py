from resic import TrojuhelnikovyResic, State

class Runner:
    def __init__(self, resic : TrojuhelnikovyResic):
        self.resice = [resic]
        self.stav = State.Unknown
        self.id = 1

    def spust_resic(self, resic : TrojuhelnikovyResic):
        resic.run(self, self.id)
        self.id += 1

    def run(self):
        self.spust_resic(self.resice[0])

        #for resic in self.resice:
        #    print(resic.stav)
        #    print(resic.promene)
        

        #odstranění chybných výsledků
        self.vysledky = [resic for resic in self.resice if resic.stav == State.Success]
        
        #vyhodnocení stavu
        if self.vysledky:
            self.stav = State.Success
        else:
            self.stav = State.Failure

        for resic in self.resice:
            if resic.stav == State.Unsolved:
                self.stav = State.Unsolved

        #print(self.stav)


    def duplicate(self, spoustec : TrojuhelnikovyResic, vysledek, poradi, moznosti : tuple):
        for moznost in moznosti[1:]:
            novy = spoustec.copy()
            novy.set(vysledek, poradi, moznost)
            self.resice.append(novy)
            self.spust_resic(novy)

    