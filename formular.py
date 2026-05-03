import pravidla
from resic import TrojuhelnikovyResic, State
from runner import Runner


class Formular:
    def __init__(self, polozky):
        self.polozky = []
        self.zarad(polozky)

        self.vysledky = []
        self.pocet_reseni = 0
        self.hlaska = None

    def zarad(self, polozky : dict):
        for promena, nazvy in polozky.items():
            if isinstance(nazvy, tuple):
                assert(len(nazvy) == 3)
                for i, nazev in enumerate(nazvy):
                    self.vytvor_polozku(promena, i, nazev)
            else:
                self.vytvor_polozku(promena, 0, nazvy)

    def vytvor_polozku(self, promena, pozice, nazev):
        assert(isinstance(promena, str))
        assert(isinstance(nazev, str))
        
        self.polozky.append({
            "promena": promena,
            "pozice" : pozice,
            "nazev" : nazev,
            "name" : promena + str(pozice),
            "hodnota" : "",
        })

    def zpracuj_hodnoty(self, zdroj):
        self.vysledky = []
        self.pocet_reseni = 0
        self.hlaska = None

        resic = TrojuhelnikovyResic()
        pocet = 0

        for pole in self.polozky:
            obsah = zdroj.get(pole["name"])
            
            if obsah not in (None, ""):
                pole["hodnota"] = obsah
                try:
                    hodnota = float(obsah)
                except ValueError:
                    self.hlaska = f"Zadanou hodnotu '{obsah}' se nepodařilo převést na číslo."
                    return
                
                pocet += 1
                resic.set(pole["promena"], pole["pozice"], hodnota)

        if pocet != 3:
            self.hlaska = "Můsíte vyplnit právě tři prvky trojúhelníku."
            return
        
        runner = Runner(resic)
        runner.run()

        self.vysledky = runner.vysledky

        match runner.stav:
            case State.Unsolved:
                self.hlaska = "Trojúhelník se nepodařilo vyřešit."
                self.vysledky = []
            
            case State.Failure:
                self.hlaska = "Trojúhelník se zadanými prvky neexistuje."
            
            case State.Success:
                self.pocet_reseni = len(self.vysledky)
                self.hlaska = None

        