from collections import namedtuple

Pole = namedtuple("Pole", ["promena", "pozice", "nazev", "name"])

class Formular:
    def __init__(self, polozky):
        self.polozky = []
        self.zarad(polozky)
        print(self.polozky)

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
        
        self.polozky.append(Pole(
            promena,
            pozice,
            nazev,
            promena + str(pozice)
        ))