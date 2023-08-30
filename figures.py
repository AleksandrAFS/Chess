from abc import ABC, abstractmethod


def is_check(figure: object, row: int, col: int) -> bool:
    pass


class Void:
    '''Пустой класс'''

    _color = None
    
    def __repr__(self) -> str:
        return '.'
    

class Figure(ABC):
    '''Базовый класс для всех фигур'''

    _whose_move = True

    def __init__(self, color: bool, matr: list[list[int], list[int]]) -> None:
        self._color = color
        self._matr = matr

    def move(self, row: int, col: int) -> bool:
        whose_move = self._whose_move
        if self._color == whose_move and self.access_check(row, col):
            if isinstance(self, King) and any(i.access_check(row, col) for i in self.last): 
                return False
            self._matr[self._x][self._y] = Void()
            self._matr[row][col] = self
            self._x, self._y = row, col
            type(self)._whose_move = (True, False)[whose_move]
            return True
        return False
        
    @abstractmethod
    def access_check(self, x: int, y: int) -> bool:
        return all(0 <= i < 8 for i in (x, y))
    
    @abstractmethod
    def __repr__(self):
        raise NotImplementedError
    

class Rook(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if (self._x == x or self._y == y) and super().access_check(x, y):

            start, end = [x] * 8, [y] * 8
        
            match x:
                case self._x:
                    select = (1, -1)[self._y > y]
                    end = range(self._y + select, y, select)
                case _:
                    select = (1, -1)[self._x > x]
                    start = range(self._x + select, x, select)
                
            if (self._matr[x][y]._color != self._color
                and all(isinstance(self._matr[i][j], Void) for i, j in zip(start, end))):
                return True
            
        return False

    def __repr__(self) -> str:
        return ('♜', '♖')[self._color]


class Queen(Figure):
    def access_check(self, x: int, y: int) -> bool:
        for figur in (Elephant, Rook):
            creats = figur(self._color, self._matr)
            creats._x, creats._y = self._x, self._y
            if creats.access_check(x, y):
                return True
        return False
    
    def __repr__(self) -> str:
        return ('♛', '♕')[self._color]


class Knight(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if (self._x - x) ** 2 + (self._y - y) ** 2 == 5 and super().access_check(x, y):
            if self._matr[x][y]._color != self._color:
                return True
        return False
            
    def __repr__(self) -> str:
        return ('♞', '♘')[self._color]
    

class King(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if abs(self._x - x) <= 1 and abs(self._y - y) <= 1 and super().access_check(x, y):
            if self._matr[x][y]._color != self._color:
                return True
        return False

    def __repr__(self) -> str:
        return ('♚', '♔')[self._color]
    

class Pawn(Figure):
    def __init__(self, *args, **kwargs) -> None:
        self.start = True
        super().__init__(*args, **kwargs)
        self.select = (1, -1)[self._color]
        self.run = (2, -2)[self._color]
        self.queen = (0, 7)[self._color]

    def access_check(self, x: int, y: int) -> bool:
        if (
               (
                (self._x - x == self.select 
                 and abs(self._y - y) <= 1) or 
                (self.start and 
                 self._x - x == self.run
                 and self._y == y and 
                 isinstance(self._matr[self._x + -self.select][y], Void))
                )
            and super().access_check(x, y)
           ):
            return self.correct(x, y, Figure if self._y != y else Void)
        
    def correct(self, row: int, col: int, goto: object = Void) -> bool:

        matr = self._matr[row]
        
        if isinstance(matr[col], goto) and matr[col]._color != self._color:

            self.start = False

            if self.queen == row:
                value = Queen(self._color, self._matr)
                value._x, value._y = row, col
                self._matr[row][col] = value
            else:
                return True
        
        return False
            
    def __repr__(self) -> str:
        return ('♟', '♙')[self._color]
            

class Elephant(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if abs(self._x - x) == abs(self._y - y) and super().access_check(x, y):  
            x_ = -1 if self._x > x else 1
            y_=  -1 if self._y > y else 1
            if (
                self._matr[x][y]._color != self._color 
                and all(
                        isinstance(self._matr[i][j], Void)
                        for i, j in zip(range(self._x + x_, x, x_), range(self._y + y_, y, y_))
                    )
            ):
                return True
        return False


    def __repr__(self) -> str:
        return ('♝', '♗')[self._color] 
