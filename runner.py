from resic import TrojuhelnikovyResic, State
from rule import Rule

class Runner:
    def __init__(self, resic : TrojuhelnikovyResic):
        self.resice = [resic]
        self.stav = State.Unknown
        self.id = 1

    def spust_resic(self, resic : TrojuhelnikovyResic):
        resic.run(self, self.id)
        self.id += 1

    def run(self, ban : Rule = None):
        #zpracování banů
        rs = self.resice[0]
        if ban:
            zaloha = rs.reset(ban)
            rs.run(None, "ban")     #větvení je zakázáno
            if rs.stav == State.Failure:
                self.stav = State.Ban
                self.vysledky = []
                return
            rs.reset(zaloha)


        #vlastní výpočet
        self.spust_resic(rs)


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



    def duplicate(self, spoustec : TrojuhelnikovyResic, vysledek, poradi, moznosti : tuple):
        for moznost in moznosti[1:]:
            novy = spoustec.copy()
            novy.set(vysledek, poradi, moznost)
            self.resice.append(novy)
            self.spust_resic(novy)

    