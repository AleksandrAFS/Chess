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
    def correct(self, row: int, col: int) -> bool:
        self._matr[self._x][self._y] = Void()
        self._matr[row][col] = self
        self._x, self._y = row, col
        return True
    
    @abstractmethod
    def access_check(self):
        raise NotImplementedError
    
    @abstractmethod
    def __repr__(self):
        raise NotImplementedError
    


class Castle(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return self._x == x or self._y == y
    
    def correct(self, row: int, col: int) -> bool | None:
        pass

    def __repr__(self):
        return ('♜', '♖')[self._color]


class Queen(Figure):
    def access_check(self, x: int, y: int) -> bool:
        _x: int = self._x
        _y: int = self._y
        return abs(_x - x) <= 1 and abs(_y - y) <= 1 or _x == x or _y == y
    
    def correct(self):
        pass

    def __repr__(self):
        return ('♛', '♕')[self._color]


class Knight(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if (
            (self._x - x) ** 2 + (self._y - y) ** 2 == 5 
            and super().access_check(x, y)
        ):
            return self.correct(x, y)
            
    def correct(self, row: int, col: int) -> bool:
        if self._matr[row][col]._color != self._color:
            return super().correct(row, col)

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
    def access_check(self, x: int, y: int) -> bool | None:
        select = [1, -1][self._color]
        
        if (
            self._x - x == select 
            and abs(self._y - y) <= 1 
            and super().access_check(x, y)
           ):
            return self.correct(x, y, Figure if self._y != y else Void)
           
    def correct(self, row: int, col: int, goto: object = Void) -> bool | None:
        matr = self._matr[row]
        
        if (
            isinstance(matr[col], goto)
            and matr[col]._color != self._color
            ):
              return super().correct(row, col)
            
    def __repr__(self) -> str:
        return ('♟', '♙')[self._color]
            

class Elephant(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if (
            abs(self._x - x) == abs(self._y - y)
            and super().access_check(x, y)
        ):  
            print(1)
            return self.correct(x, y)

    def correct(self, x, y):
        x_ = -1 if self._x > x else 1
        y_=  -1 if self._y > y else 1
        if (
            self._matr[x][y]._color != self._color 
            and all(
                    isinstance(self._matr[i][j], Void)
                    for i, j in zip(range(self._x + x_, x, x_), range(self._y + y_, y, y_))
                )
        ):
            return super().correct(x, y)

    def __repr__(self):
        return ('♝', '♗')[self._color]
