#!/usr/bin/env python3

""" Solver for the game """

import itertools
from typing import Literal, Tuple, Optional

from verificators import Verificator, Compare, OccurenceVal, Smallest, Compare2
from game import Game
from utils import Combi, Verifs, Shape

class Solver:
    """ Define a solver for a game """
    combi: Combi
    combi_use: Literal[0, 1, 2, 3] = 0
    possibles: set[Combi]
    results: list[tuple]
    solved: bool = False

    def __init__(self, game: Game) -> None:
        self.game = game
        self.possibles = set(map(lambda t: Combi(*t), itertools.product([1, 2, 3, 4, 5], repeat=3)))
        self.results = list(itertools.product(*[verificator.get_results() for verificator in self.get_verifs()]))
        self.all_combis = self.possibles.copy()

    def is_finished(self) -> bool:
        """ Check if the game is finished """
        return self.solved

    def get_verifs(self) -> list[Verificator]:
        """ Get verificators """
        return [list(verif.values())[0] for verif in self.game.list_verificators()]

    def set_combinaison(self, combinaison: Combi) -> None:
        """ Set the combinaison to verify """
        # print(f"Setting combinaison: {combinaison}")
        self.combi = combinaison
        self.combi_use = 0

    def verify(self, choice: Verificator) -> bool:
        """ Verify the combinaison for the verificator """
        if self.combi_use == 3:
            raise ValueError("Combinaison used 3 times already")
        self.combi_use += 1

        # print(f"    - {choice}")
        res = choice.verify(self.game.solution, self.combi)
        choice.discard(self.possibles, self.combi, res)

        return res

    def solve(self):
        """ Solve the game """
        best_combi, best_verifs = self.min_max_solve()
        tries = []

        self.set_combinaison(best_combi)
        for verif in best_verifs:
            res = self.verify(verif)
            tries.append((verif, res))

        if len(self.possibles) == 1:
            self.solved = True
        return best_combi, tries

    def min_max_solve(self) -> Tuple[Combi, tuple[Verificator, ...]]:
        """ Returns the best choice possible for a given state """
        min_max_value = 125
        solution_combi = None
        solution_verifs = None

        # get all combinations of verificators (len 1, 2 or 3)
        verifs = self.get_verifs()
        all_verifs_combine: list[tuple[Verificator]] = []
        for repeat in range(1, 4):
            combinations = itertools.combinations(verifs, repeat)
            all_verifs_combine.extend(combinations)

        # loop throug verificators
        for possible_verif in all_verifs_combine:
            max_remaining = 0
            possible_solution = None

            # loop through possible combi
            for possible_try in self.possibles:

                # get all solution for given choices
                for possible_solution in self.possibles:
                    try_combi = self.possibles.copy()

                    for verif in possible_verif:
                        solution_res = verif.get_res(possible_solution)
                        try_res = verif.get_res(possible_solution)
                        verif.make_try(try_combi, try_res, try_res == solution_res)

                    # if impossible combinaison, exit
                    if not try_combi:
                        continue

                    if len(try_combi) > max_remaining:
                        max_remaining = len(try_combi)
                        for new_sol in try_combi:
                            break
                        possible_solution = new_sol

            if max_remaining < min_max_value:
                min_max_value = max_remaining
                solution_combi = possible_solution
                solution_verifs = possible_verif

        assert solution_combi is not None and solution_verifs is not None
        return solution_combi, solution_verifs


    def __get_results(self, combi: Combi) -> Optional[list]:
        """ Get the results for a combinaison """
        list_results = []
        for verif in self.get_verifs():
            result = verif.get_res(combi)
            if result is None:
                return None
            list_results.append(result)
        return list_results

    def cleanup_combinaisons(self):
        """ Assign each combinaisons to the results of verificators """
        matrix = {}
        for result in self.results:
            matrix[result] = []

        for combi in self.all_combis:
            results = self.__get_results(combi)
            if results is None:
                self.possibles.remove(combi)
                continue
            matrix[tuple(results)].append(combi)

        for i, v in matrix.items():
            if len(v) == 0:
                self.results.remove(i)
            if len(v) > 1:
                for combi in v:
                    self.possibles.remove(combi)
