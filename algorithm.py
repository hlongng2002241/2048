from abc import ABC, abstractmethod
from evaluation import Evaluation
from grid import Grid


class Algorithm(ABC):
    def __init__(self) -> None:
        super().__init__()

        self.eval = Evaluation()

    @abstractmethod
    def best_move(self, grid: Grid):
        pass