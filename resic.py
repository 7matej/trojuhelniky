from collections import defaultdict
from itertools import batched
from enum import Enum
from copy import deepcopy

from rule import Rule

class SolverError(Exception):
    pass

class State(Enum):
    Success = 0
    Failure = 1
    Unknown = 2
    Unsolved = 3

class TrojuhelnikovyResic:    
    def __init__(self, pravidla : Rule):
        self.pravidla = pravidla
        self.stav = State.Unknown
        self.promene=defaultdict(lambda:[None, None, None])


    def copy(self)->'TrojuhelnikovyResic':
        novy = TrojuhelnikovyResic(self.pravidla)
        novy.stav = self.stav
        novy.promene = deepcopy(self.promene)
        return novy
    
    def set(self, promena, poradi, hodnota):
        self.promene[promena][poradi] = hodnota
    def get(self, promena, poradi):
        return self.promene[promena][poradi]


    def run(self, runner, id):
        self.id = id
        self.runner = runner
        
        while (self.spust_pravidla()):
            if self.stav == State.Failure:
                break
        
        else:
            if self.zkontroluj_uplnost():
                self.stav = State.Success
            else:
                self.stav = State.Unsolved

        
        del self.promene["__condition"]

    def spust_pravidla(self):
        for func, vysledek, args in self.pravidla.lst:
            
            for i in range(0, 3):
                if self.promene[vysledek][i] is None:
                    if self.spust_pravidlo(func, vysledek, args, i, 1) \
                    or self.spust_pravidlo(func, vysledek, args, i, -1):
                        return True
        return False
                            

    def spust_pravidlo(self, func, vysledek, args, vysledek_poradi, smer):
        #vrátí True, pokud se pravidlo spustilo a nejde o podmínku
        
        #načte argumenty
        arglist = []
        for promena, poradi in batched(args, 2):
            hodnota = self.promene[promena][(vysledek_poradi + poradi*smer) % 3]
            if hodnota is None:
                return False
            arglist.append(hodnota)

        
        #spustí pravidlo
        try:
            vypoctena_hodnota = func(*arglist)
            
            if vysledek == '__condition':
                if not vypoctena_hodnota:
                    raise SolverError("Podmínka není splněna.")

            elif not je_cislo(vypoctena_hodnota):
                raise SolverError(f"Hodnota '{vypoctena_hodnota}' vrácená funkcí není číslo,"
                                  " nebo neprázdná n-tice čísel.")
        
        except Exception as e:
            print("")
            print("---------------------ERROR-------------------------------")
            print(f"Řešič id={self.id}")
            print(f"Funkce '{func.__name__}' při výpočtu proměnné '{vysledek}' - '{poradi}':")
            print(repr(e))
            print("Stav proměnných v době chyby:")
            print(repr(self.promene))
            print("---------------------------------------------------------")
            print("")
            self.stav = State.Failure
        else:
            if vysledek != "__condition":
                if isinstance(vypoctena_hodnota, tuple):
                    vypoctena_hodnota = odstran_duplicity(vypoctena_hodnota)
                    self.runner.duplicate(self, vysledek, vysledek_poradi, vypoctena_hodnota)
                    vypoctena_hodnota = vypoctena_hodnota[0]
                
                self.promene[vysledek][vysledek_poradi] = vypoctena_hodnota
                return True
            return False
            
        return True
    
    def zkontroluj_uplnost(self) -> bool:
        for promena in self.pravidla.povolene:
            if not promena.startswith("__") and not self.je_vyreseno(self.promene[promena]):      #__condition ignorováno
                return False
        return True

    def je_vyreseno(self, lst : list) -> bool:
        for i in lst:
            if i is None:
                return False
        return True

    



#pomocné funkce
def je_cislo(x):
    if isinstance(x, tuple):
        if x == ():
            return False
        for prvek in x:
            if not isinstance(prvek, (int, float)):
                return False
        return True
    
    return isinstance(x, (int, float))

def odstran_duplicity(puvodni : tuple):
    return tuple(set(puvodni))
