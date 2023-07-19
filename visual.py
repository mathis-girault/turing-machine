#!/usr/bin/env python3.9

import tkinter as tk
from verificators import Verificator
from game import Game
from solver import Solver
from utils import Combi

class VerificatorVisual(tk.Frame):
    """ visual representation of a verificator """

    def __init__(self, parent, verificator: Verificator):
        super().__init__(parent, bg="lightgray", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        self.label = tk.Label(self, text=str(verificator))
        self.label.grid(row=0, column=0)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, sticky="e")

        self.buttons = []
        for index, result in enumerate(verificator.get_results()):
            button = tk.Button(self.button_frame, text=str(result))
            button.grid(row=0, column=index, padx=5)
            self.buttons.append(button)


class GameVisual(tk.Frame):
    """ visual representation of a game """

    def __init__(self, parent, game: Game):
        super().__init__(parent, bg="lightblue", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        self.label = tk.Label(self, text="Game setup")
        self.label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, columnspan=2)

        for index, verificator_dict in enumerate(game.list_verificators()):
            for letter, verificator in verificator_dict.items():
                letter_label = tk.Label(self, text=letter)
                letter_label.configure(bg=self['bg'], font=("Arial", 14, "bold"))
                letter_label.grid(row=index+1, column=0, padx=5, pady=5)

                verificator_label = VerificatorVisual(self, verificator)
                verificator_label.grid(row=index+1, column=1, pady=10, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(len(game.list_verificators())+1, weight=1)


class ResultsVisual(tk.Frame):
    """ Contains the results """
    max_rows = 15  # Maximum number of rows per column

    def __init__(self, parent, solver: Solver):
        super().__init__(parent, bg="white", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        self.label = tk.Label(self, text="Results")
        self.label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, columnspan=2)

        self.solver = solver

        self.results_labels = []
        self.show_results()

    def show_results(self):
        """ Shows the results """
        for label in self.results_labels:
            label.destroy()
        self.results_labels = []

        current_col = 0
        current_row = 1

        list_possibles = list(self.solver.possibles)
        list_possibles.sort()

        for index, combi in enumerate(list_possibles):
            label = tk.Label(self, text=str(combi))
            label.grid(row=current_row, column=current_col, pady=3, padx=3)
            self.results_labels.append(label)
            current_row = ((index + 1) % self.max_rows) + 1

class HistoryVisual(tk.Frame):
    """ Visual representation of the history played """
    def __init__(self, parent):
        super().__init__(parent, borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        label = tk.Label(self, text="History")
        label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        label.grid(row=0, column=0, columnspan=2)

        self.row_index = 1

    def add_history(self, chosen_combi: Combi, chosen_verifs: list[tuple[Verificator, bool]]):
        """ Adds a history to the visual """
        if self.row_index > 1:
            empty_label = tk.Label(self, text="")
            empty_label.grid(row=self.row_index, column=0, columnspan=2, pady=5)
            self.row_index += 1

        label_combi = tk.Label(self, text=f"{chosen_combi} :")
        label_combi.grid(row=self.row_index, column=0, padx=5, pady=0)

        for index, result in enumerate(chosen_verifs):
            label_verif = tk.Label(self, text=f"{result[0].get_slot()} - {result[1]}")
            label_verif.grid(row=self.row_index + index, column=1, padx=5, pady=0, sticky="w")

        self.row_index += len(chosen_verifs)

class SolverVisual(tk.Frame):
    """ Visual representation of the solver """

    def __init__(self, parent, solver: Solver, results_visual: ResultsVisual, history_visual: HistoryVisual):
        super().__init__(parent, bg="lightgreen", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        label = tk.Label(self, text="Solver")
        label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        label.grid(row=0, column=0, columnspan=2)

        self.solver = solver
        self.results_visual = results_visual
        self.history_visual = history_visual

        self.add_solving_button()

    def add_solving_button(self):
        """ Adds a button to solve the game """
        def solve_try():
            """ Solves a try """
            if not self.solver.is_finished():
                chosen_combi, results = self.solver.solve()
                self.results_visual.show_results()
                self.history_visual.add_history(chosen_combi, results)

        best_try_button = tk.Button(self, text="Best Try", command=solve_try)
        best_try_button.grid(row=1, column=0, pady=5)

class MainWindow(tk.Frame):
    """ Main visual window """
    game: Game
    solver: Solver

    def __init__(self, parent, game: Game):
        super().__init__(parent, bg="white", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        self.game = game
        self.solver = Solver(game)
        self.solver.cleanup_combinaisons()

        self.add_elements()

    def add_elements(self):
        """ Add the various visual elements """
        game_visual = GameVisual(self, self.game)
        game_visual.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        results_visual = ResultsVisual(self, self.solver)
        results_visual.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        history_visual = HistoryVisual(self)
        history_visual.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        solver_visual = SolverVisual(self, self.solver, results_visual, history_visual)
        solver_visual.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
