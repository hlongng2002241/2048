from .score import Score


class State:
    def __init__(self, file_path: str, mode) -> None:
        """
        Parameters
        ----------
            mode: State's mode
                can be "load" or "save
        """
        self.f_load         = None
        self.f_save         = None
        self.__idx          = 0
        self.mode           = mode
        self.open_file(file_path, mode)
    
    def open_file(self, file_path: str, mode: str):
        """
        Parameters
        ----------
            mode: State's mode
                can be "load" or "save
        """        
        self.close_file(mode)

        if mode == "load":
            self.f_load     = open(file_path, "r")
            self.__idx      = 0
            return
        
        if mode == "save":
            self.f_save     = open(file_path, "w")
            self.__idx      = 0
            return
        
        raise ValueError(f"not found mode: {mode}" )

    def close_file(self, mode: str):
        if mode == "load":
            if self.f_load is not None and self.f_load.closed is False:
                self.f_load.close()
            return

        if mode == "save":
            if self.f_save is not None and self.f_save.closed is False:
                self.f_save.close()
            return
        
        raise ValueError(f"not found mode: {mode}" )

    def save_next(self, board: list[list], score: Score):
        self.f_save.write(str(self.__idx) + "\n")
        self.f_save.write(str(score.current_score) + "\n")
        self.__idx         += 1
        for row in board:
            self.f_save.write(str(row) + "\n")

    def load_next(self, board: list[list], score: Score):
        line                = self.f_load.readline()
        if len(line) == 0:
            return
        self.__idx          = int(line.split(maxsplit=1)[0])

        line                = self.f_load.readline()
        score.current_score = int(line.split(maxsplit=1)[0])
        score.num_moves     = self.__idx
        
        for r in range(4):
            line            = eval(self.f_load.readline())
            for c in range(4):
                board[r][c] = line[c]

    
    