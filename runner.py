from resic import TrojuhelnikovyResic, State

class Runner:
    def __init__(self, resic : TrojuhelnikovyResic):
        self.resice = [resic]

    def run(self):
        self.resice[0].run(self)

    def duplicate(self, spoustec, vysledek, poradi, moznosti):
        pass