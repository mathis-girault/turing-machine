from typing import Optional
from verificators import Verificator
from utils import Combi, Verifs

class Game:
    """ Define a game setup """
    solution: Combi
    A: Verificator
    B: Verificator
    C: Verificator
    D: Verificator
    E: Optional[Verificator]
    F: Optional[Verificator]

    def __init__(self, A: Verificator, B: Verificator, C: Verificator, D: Verificator, E: Optional[Verificator] = None, F: Optional[Verificator] = None) -> None:
        self.A = A
        A.set_slot("A")
        self.B = B
        B.set_slot("B")
        self.C = C
        C.set_slot("C")
        self.D = D
        D.set_slot("D")
        self.E = E
        if E is not None:
            E.set_slot("E")
        self.F = F
        if F is not None:
            F.set_slot("F")

    def set_solution(self, solution: Combi) -> None:
        """ Set the solution """
        self.solution = solution

    def list_verificators(self) -> list[dict[str, Verificator]]:
        """ Return the list of verificators """
        result = [{"A": self.A}, {"B": self.B}, {"C": self.C}, {"D": self.D}]
        result += [{"E": self.E}] if self.E is not None else []
        result += [{"F": self.F}] if self.F is not None else []
        return result

    def get_verificator(self, choice: Verifs) -> Verificator:
        """ Get the verificator for the choice """
        if choice == Verifs.A:
            return self.A
        if choice == Verifs.B:
            return self.B
        if choice == Verifs.C:
            return self.C
        if choice == Verifs.D:
            return self.D
        if choice == Verifs.E:
            if self.E is None:
                raise ValueError("E is not defined")
            return self.E
        if choice == Verifs.F:
            if self.F is None:
                raise ValueError("F is not defined")
            return self.F
        raise ValueError(f"Choice {choice} is not valid")

    def verify(self, choice: Verifs, test: Combi):
        """ Verify the test combinaison """
        if choice == Verifs.A:
            return self.A.verify(self.solution, test)
        if choice == Verifs.B:
            return self.B.verify(self.solution, test)
        if choice == Verifs.C:
            return self.C.verify(self.solution, test)
        if choice == Verifs.D:
            return self.D.verify(self.solution, test)
        if choice == Verifs.E:
            if self.E is None:
                raise ValueError("E is not defined")
            return self.E.verify(self.solution, test)
        if choice == Verifs.F:
            if self.F is None:
                raise ValueError("F is not defined")
            return self.F.verify(self.solution, test)
        raise ValueError(f"Choice {choice} is not valid")

    def __str__(self) -> str:
        output = "\n" + "==="*21 + "\n"
        output += "Game configuration:"
        output += ''.join(list(map(lambda verif: f'\n   - {list(verif.keys())[0]}: {str(list(verif.values())[0])}', self.list_verificators())))
        output += "\n" + "==="*21 + "\n"
        return output
