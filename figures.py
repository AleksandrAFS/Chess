from abc import ABC, abstractmethod


def is_check(king: object, row: int, col: int) -> bool:

    """Проверка шаха/мата королю"""
    
    obj: object = king._matr[row][col]
    king._matr[row][col] = king

    res: bool = any(figure.access_check(row, col) 
                    for figure in king.enemy_figures
                    if isinstance(figure, Figure) and (figure._x, figure._y) != (row, col))
  
    king._matr[row][col] = obj
    return res


def is_checkmate(self: object, x: int, y: int) -> bool:

    your_king = self.your_king
    coordinates: tuple = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x - 1, y - 1),
                          (x + 1, y - 1), (x + 1, y + 1))
    
    for enemy_figure in self.enemy_figures:
        for row, col in coordinates:

            if enemy_figure.access_check(row, col):

                obj: object = self._matr[row][col]
                self._matr[enemy_figure._x][enemy_figure._y] = Void()
                self._matr[row][col] = enemy_figure

                check = is_check(your_king, x, y)
                
                self._matr[enemy_figure._x][enemy_figure._y] = enemy_figure
                self._matr[row][col] = obj

                if not check:
                    return False
                
    return True


def pawn_queen(self) -> None:
    
    """Перевоплащение пешки в ферзя"""
    
    self.start = False
    
    if self.queen == self._x:
        value = Queen(self._color, self._matr)
        value._x, value._y = self._x, self._y
        self._matr[self._x][self._y] = value
        self.qn[self.qn.index(self)] = value
        value.enemy_figures, value.your_king = self.enemy_figures, self.your_king

        
class Void:
    '''Пустой класс'''

    _color = None
    
    def __repr__(self) -> str:
        return '.'
    

class Figure(ABC):
    '''Базовый класс для всех фигур'''

    _whose_move: bool = True
    
    def __init__(self, color: bool, matr: list[list[int], list[int]]) -> None:
        self._color: bool = color
        self._matr: list = matr

        def move(self, row: int, col: int) -> bool:

        whose_move: bool = Figure._whose_move

        if self._color == whose_move and self.access_check(row, col):
            
            del_figur = self._matr[row][col]
            self._matr[self._x][self._y] = Void()
            self._matr[row][col] = self

            if isinstance(del_figur, Figure):
                del self.enemy_figures[self.enemy_figures.index(del_figur)]
            
            value = self.your_king
            _x, _y =  (row, col) if isinstance(self, King) else (value._x, value._y)
            if is_check(value, _x, _y):

                if is_checkmate(self, _x, _y):
                    print(f'''{('Чёрные', 'Белые')[whose_move]} победили! 
                          Был поставлен мат {('Белым', 'Чёрным')[whose_move]}''')
                    self.your_board.surrender(determine_winner=int(whose_move))
                    print('Начните игру заново')
                    return False

                self._matr[row][col] = del_figur
                self._matr[self._x][self._y] = self

                return False
            
            self._x, self._y = row, col
            
            Figure._whose_move = not whose_move

            if isinstance(self, Pawn):
                pawn_queen(self)
                
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
        return (
                (
                 (self._x - x == self.select 
                 and abs(self._y - y) <= 1) or 
                 (self.start and 
                 self._x - x == self.run
                 and self._y == y and 
                 isinstance(self._matr[self._x + -self.select][y], Void))
                )
                 and super().access_check(x, y) and 
                 isinstance(self._matr[x][y], Figure if self._y != y else Void) 
                 and self._matr[x][y]._color != self._color
        )
            
    def __repr__(self) -> str:
        return ('♟', '♙')[self._color]
            

class Elephant(Figure):
    def access_check(self, x: int, y: int) -> bool:
        if abs(self._x - x) == abs(self._y - y) and super().access_check(x, y):  
            x_: int = -1 if self._x > x else 1
            y_: int =  -1 if self._y > y else 1
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
