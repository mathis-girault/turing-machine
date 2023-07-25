#!/usr/bin/env python3.9

import tkinter as tk
from visual import MainWindow
from verificators import Compare, OccurenceVal, SmallestShape, Compare2
from utils import Combi, Shape, Verifs
from game import Game
from solver import Solver


class Main:
    """ Main game """
    def __init__(self, game: Game):
        self.game = game
        self.solver = Solver(self.game)
        self.solver.cleanup_combinaisons()

    def visualize(self):
        """ Creates the main window """
        window = tk.Tk()
        window.title("Welcome to the solver")

        # Add the visuals
        main_window = MainWindow(window, self.game)
        main_window.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Start the main event loop
        window.mainloop()


if __name__ == "__main__":
    new_game = Game()
    new_game.set_verificator(Verifs.A, Compare(Shape.CARRE, 4))
    new_game.set_verificator(Verifs.B, OccurenceVal(3))
    new_game.set_verificator(Verifs.C, Compare2(Shape.TRIANGLE, Shape.CARRE))
    new_game.set_verificator(Verifs.D, SmallestShape())

    new_game.set_solution(Combi(2, 4, 1))
    # new_game.set_solution(Combi(4, 4, 3))
    # new_game.set_solution(Combi(5, 4, 5))

    main_game = Main(new_game)
    main_game.visualize()
