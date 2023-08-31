from itertools import product
from figures import King, Knight, Elephant, Queen, Pawn, Rook, Void


class Board:
    """Шахматная доска, раставляет 
       все экземпляры фигур на поле"""
       
    def __init__(self) -> None:
        self.matrix = [[Void()] * 8 for _ in range(8)]
        self.types = (Rook, Knight, Elephant)
        self.last = ([], [])
        self.kinges = []
        
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
        
         #установка короля и королевы
        
        self.matrix[side - 1][3] = Queen(color, self.matrix)
        king = King(color, self.matrix)
        self.matrix[side - 1][4] = king
        self.kinges.append(king)
        
        if color is False:
            self.matrix[side - 1:] = [*reversed(self.matrix[side - 1:])]
    
    def end(self) -> None:
        for i, j in product(range(8), repeat=2):
            obj = self.matrix[i][j]
            if not isinstance(obj, Void):
                obj._x, obj._y = i, j
                obj.last = self.last[not obj._color]
                self.last[obj._color].append(obj)
                obj.your_king = self.kinges[not obj._color]
                
    def __repr__(self) -> str:
        return '\n'.join(' '.join(map(str, r)) for r in reversed(self.matrix))
