from itertools import product
from figures import Rook, Knight, Elephant, Void, Pawn, King, Queen


class Board:
    """Шахматная доска, раставляет 
       все экземпляры фигур на поле"""
       
    def __init__(self) -> None:
        self.matrix = [[Void()] * 8 for _ in range(8)]
        self.types = (Rook, Knight, Elephant)
        
        self.create(1, True)
        self.create(7, False)
        
        self.end()

    def __getitem__(self, index: int):
        return self.matrix[index]
            
    def create(self, side: int, color: bool) -> None:
        #установка пешек
   
        for value in range(8):
            self.matrix[side][value] = Pawn(color, self.matrix)
        
        #устанока экземпляров классов из кортежа self.types
        
        for key in range(3):
            self.matrix[side - 1][key] = self.types[key](color, self.matrix)
            self.matrix[side - 1][~key] = self.types[key](color, self.matrix)
            
        #установка кароля и королевы
        
        self.matrix[side - 1][3] = Queen(color, self.matrix)
        self.matrix[side - 1][4] = King(color, self.matrix)
        
        if color is False:
            self.matrix[side - 1:] = [*reversed(self.matrix[side - 1:])]
    
    def end(self) -> None:
        for i, j in product(range(8), repeat=2):
            obj = self.matrix[i][j]
            obj._x, obj._y = i, j

    def __repr__(self) -> str:
        return '\n'.join(' '.join(map(str, r)) for r in reversed(self.matrix))
