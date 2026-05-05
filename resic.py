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
    Ban = 4

class TrojuhelnikovyResic:    
    def __init__(self, pravidla : Rule, print_error = True):
        self.pravidla = pravidla
        self.stav = State.Unknown
        self.promene=defaultdict(lambda:[None, None, None])
        self.print_error = print_error

    def reset(self, pravidla : Rule = None) -> Rule:
        #! zachovává proměnné, vrací původní pravidla
        self.stav = State.Unknown
        puvodni = self.pravidla
        if pravidla:
            self.pravidla = pravidla
        return puvodni

    def copy(self)->'TrojuhelnikovyResic':
        novy = TrojuhelnikovyResic(self.pravidla, self.print_error)
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
    



    def nacti_argumenty(self, args, vysledek_poradi, smer):
        arglist = []
        for promena, poradi in batched(args, 2):
            hodnota = self.promene[promena][(vysledek_poradi + poradi*smer) % 3]
            if hodnota is None:
                return None
            arglist.append(hodnota)
        
        return arglist          


    def spust_pravidlo(self, func, vysledek, args, vysledek_poradi, smer):
        #vrátí True, pokud se pravidlo spustilo a nejde o podmínku
        
        #načte argumenty
        arglist = self.nacti_argumenty(args, vysledek_poradi, smer)
        if arglist is None:
            return False

        
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
            if self.print_error:
                print("")
                print("---------------------ERROR-------------------------------")
                print(f"Řešič id={self.id}")
                print(f"Funkce '{func.__name__}' při výpočtu proměnné '{vysledek}' - '{vysledek_poradi}':")
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
    

        
    def test(self):
        #zkontroluje konzistenci pravidel
        for func, vysledek, args in self.pravidla.lst:
            if vysledek == "__condition":
                continue

            for i in range(0, 3):
                self.test_pravidlo(func, vysledek, args, i, 1)
                self.test_pravidlo(func, vysledek, args, i, -1)

    def test_pravidlo(self, func, vysledek, args, vysledek_poradi, smer):
        zaloha = self.promene[vysledek][vysledek_poradi]
        self.promene[vysledek][vysledek_poradi] = None

        hodnota = func(*self.nacti_argumenty(args, vysledek_poradi, smer))

        zkontroluj(hodnota, zaloha)
        self.promene[vysledek][vysledek_poradi] = zaloha




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


def zkontroluj(vysledek, puvodni):
    tolerance = 0.01

    if isinstance(vysledek, tuple):
        for x in vysledek:
            if abs(x - puvodni) < tolerance:
                break
        else:
            raise AssertionError
    
    else:
        assert(abs(vysledek - puvodni) < tolerance)
