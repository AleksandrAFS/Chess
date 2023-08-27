from abc import ABC, abstractmethod


class Void:
    _color = None
    
    def __repr__(self):
        return ' '


class Figure(ABC):
    def __init__(self, color: bool, matr: list[list[int], list[int]]):
        self._color = color
        self._matr = matr

    @abstractmethod
    def access_check(self):
        raise NotImplementedError
    
    @abstractmethod
    def correct(self):
        raise NotImplementedError
    
    @abstractmethod
    def __repr__(self):
        raise NotImplementedError
    

class Elephant(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return abs(self._x - x) == abs(self._y - y)

    def correct(self):
        pass

    def __repr__(self) -> str:
        return ('♝', '♗')[self._color]


class Castle(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return self._x == x or self._y == y
    
    def correct(self):
        pass

    def __repr__(self) -> str:
        return ('♜', '♖')[self._color]


class Queen(Figure):
    def access_check(self, x: int, y: int) -> bool:
        _x: int = self._x
        _y: int = self._y
        return abs(_x - x) <= 1 and abs(_y - y) <= 1 or _x == x or _y == y
    
    def correct(self):
        pass

    def __repr__(self) -> str:
        return ('♛', '♕')[self._color]


class Knight(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return (self._x - x) ** 2 + (self._y - y) ** 2 == 5
    
    def correct(self):
        pass

    def __repr__(self) -> str:
        return ('♞', '♘')[self._color]
    

class King(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return abs(self._x - x) <= 1 and abs(self._y - y) <= 1
    
    def correct(self):
        pass

    def __repr__(self) -> str:
        return ('♚', '♔')[self._color]
    

class Pawn(Figure):
    def access_check(self, x: int, y: int) -> bool:
        select = [1, -1][self._color]
        prod = all(0 <= i < 8 for i in (x, y))
        
        if (
            self._x - x == select 
            and abs(self._y - y) <= 1 
            and prod
           ):
            self.correct(x, y, Figure if self._y != y else Void)
           
    def correct(self, row: int, col: int, goto: object = Void) -> bool:
        matr = self._matr[row]
        
        if (
            isinstance(matr[col], goto)
            and matr[col]._color != self._color
            ):
              self._matr[self._x][self._y] = Void()
              self._matr[row][col] = self
              self._x, self._y = row, col
            
    def __repr__(self) -> str:
        return ('♟', '♙')[self._color]