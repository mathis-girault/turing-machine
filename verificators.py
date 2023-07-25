import abc
from enum import Enum
from typing import Set, Optional, Union
from utils import Combi, Shape, CombiVal

class Verificator(abc.ABC):
    """ Define a verificator """
    solved: bool = False
    results: list[Union[str, int, Shape]]
    slot: str

    @abc.abstractmethod
    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        pass

    @abc.abstractmethod
    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        pass

    @abc.abstractmethod
    def make_try(self, possibles: Set[Combi], result, is_true: bool) -> None:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

    @abc.abstractmethod
    def get_res(self, combinaison: Combi) -> Optional[Union[str, int, Shape]]:
        pass

    def get_results(self) -> list[Union[str, int, Shape]]:
        """ Return the list of results """
        return self.results

    def set_slot(self, slot_name: str):
        """ Set the slot name """
        self.slot = slot_name
    
    def get_slot(self) -> str:
        """ Return the slot name """
        return self.slot


class Compare(Verificator):
    """ Define a verificator that compare a shape's value to a given value """
    def __init__(self, shape: Shape, value: CombiVal) -> None:
        self.shape: Shape = shape
        self.value: CombiVal = value
        self.results = ["<", "=", ">"]

    def __comp(self, combinaison: Combi) -> str:
        if combinaison.get_shape(self.shape) > self.value:
            return ">"
        if combinaison.get_shape(self.shape) < self.value:
            return "<"
        return "="

    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        res = self.__comp(solution) == self.__comp(combinaison)
        self.solved = self.solved or res
        return res

    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        """ Discard all combinaison that don't match the result """
        comp = self.__comp(combinaison)
        to_remove = set()
        for possible in possibles:
            if self.__comp(possible) == comp:
                if not result:
                    to_remove.add(possible)
            else:
                if result:
                    to_remove.add(possible)
        possibles.difference_update(to_remove)

    def make_try(self, possibles: Set[Combi], result: str, is_true: bool) -> None:
        """ Make a try to find the solution """
        assert result in self.results
        to_discard = set()
        for possible in possibles:
            if (self.__comp(possible) != result) is is_true:
                to_discard.add(possible)
        possibles.difference_update(to_discard)

    def get_res(self, combinaison: Combi) -> Union[str, int, Shape]:
        """ Return the result for combinaison """
        return self.__comp(combinaison)

    def __repr__(self) -> str:
        return f"Verifying value of shape {self.shape.value} compared to {self.value}"

class OccurenceVal(Verificator):
    """ Define a verificator that check the number of occurence of a value """
    def __init__(self, value: CombiVal) -> None:
        self.value: CombiVal = value
        self.results = [0, 1, 2, 3]

    def __calc_occurence(self, combinaison: Combi) -> int:
        """ Calculate the maximum occurence """
        return sum(1 for shape in Shape.list_shapes() if combinaison.get_shape(shape) == self.value)

    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        res = self.__calc_occurence(solution) == \
                self.__calc_occurence(combinaison)
        self.solved = self.solved or res
        return res

    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        """ Discard all combinaison that don't match the result """
        nb_occ = self.__calc_occurence(combinaison)
        to_remove = set()
        for possible in possibles:
            if possible.count(self.value) == nb_occ:
                if not result:
                    to_remove.add(possible)
            else:
                if result:
                    to_remove.add(possible)
        possibles.difference_update(to_remove)

    def make_try(self, possibles: Set[Combi], result: int, is_true: bool) -> None:
        """ Make a try to find the solution """
        assert result in self.results
        to_discard = set()
        for possible in possibles:
            if (self.__calc_occurence(possible) != result) is is_true:
                to_discard.add(possible)
        possibles.difference_update(to_discard)


    def get_res(self, combinaison: Combi) -> Union[str, int, Shape]:
        """ Return the result for combinaison """
        return self.__calc_occurence(combinaison)

    def __repr__(self) -> str:
        return f"Verifying occurence for number {self.value}"

class OccurenceAll(Verificator):
    """ Define a verificator that checks if maximum occurence is 1, 2 or 3 """
    def __init__(self):
        self.results = [1, 2, 3]

    def __calc_occurence(self, combinaison: Combi) -> int:
        """ Calculate the maximum occurence """
        return max(sum(1 for shape in Shape.list_shapes() if combinaison.get_shape(shape) == value) for value in range(1, 6))

    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        res = self.__calc_occurence(solution) == self.__calc_occurence(combinaison)
        self.solved = self.solved or res
        return res

    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        """ Discard all combinaison that don't match the result """
        nb_occ = self.__calc_occurence(combinaison)
        to_remove = set()
        for possible in possibles:
            if any(possible.count(element) == nb_occ for element in range(1, 6)):
                if not result:
                    to_remove.add(possible)
            else:
                if result:
                    to_remove.add(possible)
        possibles.difference_update(to_remove)

    def make_try(self, possibles: Set[Combi], result: int, is_true: bool) -> None:
        """ Make a try to find the solution """
        assert result in self.results
        to_discard = set()
        for possible in possibles:
            if (self.__calc_occurence(possible) != result) is is_true:
                to_discard.add(possible)

        possibles.difference_update(to_discard)

    def get_res(self, combinaison: Combi) -> Union[str, int, Shape]:
        """ Return the result for combinaison """
        return self.__calc_occurence(combinaison)

    def __repr__(self) -> str:
        return "Verifying number of identical numbers"


class SmallestShape(Verificator):
    """ Define a verificator that checks which shape is the smallest """
    def __init__(self):
        self.results = [Shape.CARRE, Shape.ROND, Shape.TRIANGLE]

    def __calc_smallest(self, combinaison: Combi) -> Optional[Shape]:
        """ Calculate the maximum occurence """
        min_val = 6
        min_shape = None
        crit_flag = False
        for elem in combinaison:
            for key, value in elem.items():
                if value < min_val:
                    min_val = value
                    crit_flag = False
                    min_shape = key
                elif value == min_val:
                    crit_flag = True
        if crit_flag:
            return None
        return min_shape

    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        assert self.__calc_smallest(solution) is not None
        res = self.__calc_smallest(solution) == self.__calc_smallest(combinaison)
        self.solved = self.solved or res
        return res

    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        """ Discard all combinaison that don't match the result """
        min_shape = self.__calc_smallest(combinaison)
        to_remove = set()
        for possible in possibles:
            if self.__calc_smallest(possible) == min_shape:
                if not result:
                    to_remove.add(possible)
            else:
                if result:
                    to_remove.add(possible)
        possibles.difference_update(to_remove)

    def make_try(self, possibles: Set[Combi], result: Shape, is_true: bool) -> None:
        """ Make a try to find the solution """
        assert result in self.results
        to_discard = set()
        for possible in possibles:
            if (self.__calc_smallest(possible) != result) is is_true:
                to_discard.add(possible)

        possibles.difference_update(to_discard)

    def get_res(self, combinaison: Combi) -> Optional[Union[str, int, Shape]]:
        """ Return the result for combinaison """
        return self.__calc_smallest(combinaison)

    def __repr__(self) -> str:
        return "Verifying which shape is SmallestShape"


class Compare2(Verificator):
    """ Define a verificator that checks comparison between two shapes """
    def __init__(self, shape1: Shape, shape2: Shape) -> None:
        self.shape1: Shape = shape1
        self.shape2: Shape = shape2
        self.results = ["<", "=", ">"]

    def __comp2(self, combinaison: Combi) -> str:
        """ Calculate the maximum occurence """
        if combinaison.get_shape(self.shape1) > combinaison.get_shape(self.shape2):
            return ">"
        if combinaison.get_shape(self.shape1) < combinaison.get_shape(self.shape2):
            return "<"
        return "="

    def verify(self, solution: Combi, combinaison: Combi) -> bool:
        res = self.__comp2(solution) == self.__comp2(combinaison)
        self.solved = self.solved or res
        return res

    def discard(self, possibles: Set[Combi], combinaison: Combi, result: bool) -> None:
        """ Discard all combinaison that don't match the result """
        comp = self.__comp2(combinaison)
        to_remove = set()
        for possible in possibles:
            if self.__comp2(possible) == comp:
                if not result:
                    to_remove.add(possible)
            else:
                if result:
                    to_remove.add(possible)
        possibles.difference_update(to_remove)

    def make_try(self, possibles: Set[Combi], result: str, is_true: bool) -> None:
        """ Make a try to find the solution """
        assert result in self.results
        to_discard = set()
        for possible in possibles:
            if (self.__comp2(possible) != result) is is_true:
                to_discard.add(possible)

        possibles.difference_update(to_discard)

    def get_res(self, combinaison: Combi) -> Union[str, int, Shape]:
        """ Return the result for combinaison """
        return self.__comp2(combinaison)

    def __repr__(self) -> str:
        return f"Comparing value between {self.shape1.value} and {self.shape2.value}"



class AllVerificators(Enum):
    """ Define all verificators """
    COMPARE = Compare
    COMPARE2 = Compare2
    OCCURENCEVAL = OccurenceVal
    SMALLESTSHAPE = SmallestShape

    @classmethod
    def get_all_verificators(cls) -> list:
        role_names = [member for _, member in cls.__members__.items()]
        return role_names


verificator_classes = {
    "Compare": Compare,
    "Compare2": Compare2,
    "OccurenceVal": OccurenceVal,
    "SmallestShape": SmallestShape
}