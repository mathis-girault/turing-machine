#!/usr/bin/env python3.9

import tkinter as tk
from visual import MainWindow
from verificators import Compare, OccurenceVal, Smallest, Compare2
from utils import Combi, Shape
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
    verif_a = Compare(Shape.CARRE, 4)
    verif_b = OccurenceVal(3)
    verif_c = Compare2(Shape.TRIANGLE, Shape.CARRE)
    verif_d = Smallest()
    new_game = Game(verif_a, verif_b, verif_c, verif_d)
    new_game.set_solution(Combi(2, 4, 1))
    # new_game.set_solution(Combi(4, 4, 3))
    # new_game.set_solution(Combi(5, 4, 5))

    main_game = Main(new_game)
    main_game.visualize()
