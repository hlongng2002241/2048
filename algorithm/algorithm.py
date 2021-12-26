from abc import ABC, abstractmethod
from . evaluation import Evaluation
from game.grid import Grid


class Algorithm(ABC):
    def __init__(self, max_depth: int) -> None:
        """
        This is an abstract class, used to declared all important methods and object such as evaluation
        and maximum depth
        
        Parameters
        ----------
            max_depth: int
                maximum depth search of algorithm
        """
        super().__init__()

        self.eval       = Evaluation()
        self.max_depth  = max_depth

    @abstractmethod
    def best_move(self, grid: Grid) -> int:
        """
        Calculate and implement the best move for given grid state
        
        Parameters
        ----------
            grid: Grid
                current grid state

        Returns
        -------
            move direction: int 
                can be 0 : Up, 1 : Down, 2 : Left, 3 : Right
        """
        pass

    def set_max_depth(self, depth: int):
        self.max_depth  = depth
