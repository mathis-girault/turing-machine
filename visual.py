#!/usr/bin/env python3.9

import inspect
import tkinter as tk
from verificators import Verificator, verificator_classes
from game import Game
from solver import Solver
from utils import Combi, Verifs, Shape

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
    nb_verificators: int = 4

    def __init__(self, parent, game: Game):
        super().__init__(parent, bg="lightblue", borderwidth=1, relief=tk.SOLID, padx=10, pady=10)
        self.label = tk.Label(self, text="Game setup")
        self.label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, columnspan=2)
        self.game = game

        for i in range(self.nb_verificators):
            self.add_verificator_selector(i)

        self.add_verificator_button = tk.Button(self, text="Add Verificator", command=self.new_verificator)
        self.add_verificator_button.grid(row=self.nb_verificators+1, column=0, columnspan=2, pady=5)


    def new_verificator(self):
        """ Adds a verificator """
        self.nb_verificators += 1

        if self.nb_verificators > 6:
            self.add_verificator_button.destroy()
        else:
            self.add_verificator_button.grid(row=self.nb_verificators+1, column=0, columnspan=2, pady=5)

        self.add_verificator_selector(self.nb_verificators - 1)


    def add_verificator_selector(self, index: int):
        """ Adds a verificator selector """
        verif_letter = chr(ord('A') + index)

        letter_label = tk.Label(self, text=verif_letter)
        letter_label.configure(bg=self['bg'], font=("Arial", 14, "bold"))
        letter_label.grid(row = index + 1, column=0, padx=5, pady=5)

        verificator_visual = VerificatorSelector(self, self.game, Verifs(verif_letter))
        verificator_visual.grid(row = index + 1, column=1, pady=10, sticky="ew")

class VerificatorSelector(tk.Frame):
    """ Visual representation of a verificator selector """
    choices = list(verificator_classes.keys())
    my_params = []

    def __init__(self, parent: tk.Frame, game: Game, slot: Verifs):
        super().__init__(parent, bg="#f88", borderwidth=1, relief=tk.SOLID, padx=10, pady=2)
        self.label = tk.Label(self, text="Verificator Selector")
        self.label.configure(bg=self['bg'], font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=3)

        self.game = game
        self.slot = slot

        self.verificator_option = tk.StringVar(self)
        self.verificator_option.set(self.choices[0])

        self.dropdown = tk.OptionMenu(self, self.verificator_option, *self.choices, command=self.select_option)
        self.dropdown.grid(row=1, column=0, pady=5)

        button = tk.Button(self, text="Add", command=self.apply_selection)
        button.grid(row=1, column=1, pady=5, padx=5)

        self.select_option(self.verificator_option.get())

    def select_option(self, selected_verificator):
        """ Selects the option """
        self.verificator_option.set(selected_verificator)
        class_signature = inspect.signature(verificator_classes[self.verificator_option.get()])

        for widgets in self.my_params:
            widgets[0].destroy()
            widgets[1].destroy()
        self.my_params = []

        for index, (param_name, param) in enumerate(class_signature.parameters.items()):
            if param_name == "self":
                continue

            choices = list(param.annotation.__args__ if hasattr(param.annotation, "__args__") else list(map(lambda shape: shape.value, list(param.annotation))))

            selected_option = tk.StringVar()
            selected_option.set(choices[0])
            params_drop_down = tk.OptionMenu(self, selected_option, *choices)
            params_drop_down.grid(row = 2 + index, column=1, columnspan=2)

            param_label = tk.Label(self, text=param_name)
            param_label.grid(row = 2 + index, column=0)

            self.my_params.append([params_drop_down, param_label, selected_option])

    def apply_selection(self):
        """ Selects the option """
        selected_value = self.verificator_option.get()
        signature = list(map(lambda param: int(param) if param.isdigit() else Shape.get_shape(param), [widgets[2].get() for widgets in self.my_params]))
        new_verificator = verificator_classes[selected_value](*signature)

        self.game.set_verificator(self.slot, new_verificator)

        # Clear all widgets
        for widgets in self.my_params:
            widgets[0].destroy()
            widgets[1].destroy()
        self.dropdown.destroy()

        verificator_label = VerificatorVisual(self, new_verificator)
        verificator_label.grid(row=1, column=1, pady=10, sticky="ew")



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
        game_visual.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

        results_visual = ResultsVisual(self, self.solver)
        results_visual.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky="nsew")

        history_visual = HistoryVisual(self)
        history_visual.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        solver_visual = SolverVisual(self, self.solver, results_visual, history_visual)
        solver_visual.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
