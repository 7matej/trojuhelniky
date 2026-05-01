from collections import defaultdict
from itertools import batched
from enum import Enum

class SolverError(Exception):
    pass

class State(Enum):
    Success = 0
    Failure = 1
    Unknown = 2

class TrojuhelnikovyResic:
    def __init__(self, povolene_promene : set):
        povolene_promene.add("__condition")
        self.povolene = povolene_promene
        self.stav = State.Unknown
        self.promene=defaultdict(lambda:[None, None, None])
        self.pravidla=[]


    def rule(self, vysledek, *parametry):
        args=parametry

        if len(args) % 2 != 0:
            raise ValueError("počet parametrů metody rule musí být sudý")
        
        if vysledek not in self.povolene:
            raise ValueError(f"Zadaný výsledek výpočtu '{vysledek}' není mezi povolenými parametry")
        
        for i in range(len(args)//2):
            if not args[2*i] in self.povolene:
                raise ValueError(f"Parametr '{args[i]}' není mezi povolenými")
            if args[2*i+1] not in (0,1,2):
                raise ValueError(f"Číslo následující po názvu parametru musí být v rozmezí 0-2")
            
        def wrapper(func):
            self.pravidla.append((func, vysledek, args))
            return func
        return wrapper
    
    def cond(self, *parametry):
        return self.rule("__condition", *parametry)


    def run(self, runner):
        self.runner = runner
        
        while (self.stav != State.Failure):
            if not self.spust_pravidla():
                break
        
        del self.promene["__condition"]

    def spust_pravidla(self):
        for func, vysledek, args in self.pravidla:
            
            for i in range(0, 3):
                if self.promene[vysledek][i] is None:
                    if self.spust_pravidlo(func, vysledek, args, i, 1) \
                    or self.spust_pravidlo(func, vysledek, args, i, -1):
                        return True
        return False
                            

    def spust_pravidlo(self, func, vysledek, args, vysledek_poradi, smer):
        
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

            elif not TrojuhelnikovyResic.je_cislo(vypoctena_hodnota):
                raise SolverError(f"Hodnota '{vypoctena_hodnota}' vrácená funkcí není číslo,"
                                  " nebo neprázdná n-tice čísel.")
        
        except Exception as e:
            print("")
            print("---------------------ERROR-------------------------------")
            print(f"Funkce '{func.__name__}' při výpočtu proměnné '{vysledek}' - '{poradi}':")
            print(repr(e))
            print("Stav proměnných v době chyby:")
            print(repr(self.promene))
            print("---------------------------------------------------------")
            print("")
            self.stav = State.Failure
        else:
            if vysledek != "__condition":
                if isinstance(vysledek_poradi, tuple):
                    self.runner.duplicate(vysledek, vysledek_poradi, vypoctena_hodnota)
                    vypoctena_hodnota = vypoctena_hodnota[0]
                
                self.promene[vysledek][vysledek_poradi] = vypoctena_hodnota
                return True
            
        return False

    @staticmethod
    def je_cislo(x):
        if isinstance(x, tuple):
            if x == ():
                return False
            for prvek in x:
                if not isinstance(prvek, (int, float)):
                    return False
            return True
        
        return isinstance(x, (int, float))
