from itertools import product
from figures import Castle, Knight, Elephant, Queen, Pawn, King


class Board:
    """Шахматная доска, 
       атрибут goto - по умолчанию(True) раставляет 
       все экземпляры фигур на поле"""
       
    def __init__(self) -> None:
        self.matrix = [[None] * 8 for _ in range(8)]
        self.types = (Castle, Knight, Elephant)
        
        self.create(1, True)
        self.create(7, False)
        
        self.end()
            
    def create(self, side: int, color: bool) -> None:
        #установка пешек
        for value in range(8):
            self.matrix[side][value] = Pawn(color, self.matrix)
        #устанока экземпляров классов из кортежа self.types
        for key in range(3):
            self.matrix[side - 1][key] = self.types[key](color)
            self.matrix[side - 1][~key] = self.types[key](color)
        #установка кароля и королевы
        self.matrix[side - 1][4] = Queen(color)
        self.matrix[side - 1][3] = King(color)
        
        if color is False:
            self.matrix[side - 1:] = [*reversed(self.matrix[side - 1:])]
            self.matrix[side - 1][3:5] = [*reversed(self.matrix[side - 1][3:5])]
    
    def end(self) -> None:
        for i, j in product(range(8), repeat=2):
            obj = self.matrix[i][j]
            if obj: obj._x, obj._y = i, j