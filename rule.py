from itertools import batched

class Rule:
    def __init__(self, povolene_promene : set):
        self.lst = []
        self.povolene = povolene_promene
        self.povolene.add("__condition")



    def cond(self, *parametry):
        return self.rule("__condition", *parametry)
    
    def ban(self, *parametry):
        self.cond(*parametry)(lambda *args: False)
    
    
    def rule(self, vysledek, *parametry):
        args=parametry

        if len(args) % 2 != 0:
            raise ValueError("počet parametrů metody rule musí být lichý")
        
        if vysledek not in self.povolene:
            raise ValueError(f"Zadaný výsledek výpočtu '{vysledek}' není mezi povolenými parametry")
        
        for parametr, poradi in batched(args, 2):
            if not parametr in self.povolene:
                raise ValueError(f"Parametr '{parametr}' není mezi povolenými parametry")
            if poradi not in (0,1,2):
                raise ValueError(f"Číslo následující po názvu parametru musí být v rozmezí 0-2")
            
        def dekorator(func):
            self.lst.append((func, vysledek, args))
            return func
        return dekorator
    