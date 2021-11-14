import numpy as np 

class Evaluation:

    def points_over_nonzero(self, s):
        sum = np.sum(s)
        nonzeros = len([1 for row in s for tile in row if tile != 0])
        return sum/nonzeros

    def zeros(self,s):
        return len([1 for row in s for tile in row if tile == 0])

    # def positioning_tiles(self, s):
    #     joined_list = sum(s, [])
    #     A = -1
    #     if s[0:8].zeros < s[8:16].zeros:
    #         A = 1
    #     for ele in range(0,16,A):
    #         pass
            

    def partial_mergable_tiles(self, s):
        count = 0
        for row in s:
            temp = 0
            for ele in row:
                if (ele != 0 and temp == 0) or (temp != 0 and ele != 0 and ele != temp):
                    temp = ele
                elif (ele != 0 and temp != 0 and ele == temp):
                    count += 1*ele 
                    temp = 0
        return count 

    def mergable_tiles(self, s):
        #mergable tiles base on the row of the board
        count_row = self.partial_mergable_tiles(s)
        
        #mergable tiles base on the column of the board
        count_col = self.partial_mergable_tiles([list(np.array(s)[:, i]) for i in range(0,4)])
        return count_row + count_col