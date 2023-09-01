from itertools import product
from figures import King, Knight, Elephant, Queen, Pawn, Rook, Void, Figure
from time import perf_counter
import pymysql
from connectSQL import host, db_name, password, user
from datetime import datetime


CONNECTION = pymysql.connect(
    host=host,
    port=3306, 
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)


class Board:
    """Шахматная доска, раставляет 
       все экземпляры фигур на поле и 
       позволяет взаимодействовать с ними"""

    __result = {
                Pawn: 1, Knight: 2, Rook: 3,
                Elephant: 3, King: 0, Queen: 5
               }
    
    def __init__(self) -> None:
        self.matrix = [[Void()] * 8 for _ in range(8)]
        self.types = (Rook, Knight, Elephant)
        self.last = ([], [])
        self.kinges, self.status = [], perf_counter()
        self.start = str(datetime.now())
        
        self.create(1, True)
        self.create(7, False)
        
        self.end()

    def __getitem__(self, index: int):
        return self.matrix[index]
            
    def create(self, side: int, color: bool) -> None:
        
        #установка пешек
   
        for value in range(8):
            pawn = Pawn(color, self.matrix)
            self.matrix[side][value] = pawn
            pawn.qn = self.last[color]
        
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
        
    def surrender(self, *, determine_winner: bool = True) -> None:
        """Запись в SQL базу данных результата поединка и 
        удаление данных о фигурах и таблице"""
        
        x = sum(self.__result[i.__class__] for i in self.last[0])
        y = sum(self.__result[i.__class__] for i in self.last[1])
        
        win = (
            not Figure._whose_move 
            if determine_winner else 
            (x > y, x < y, x == y).index(True)
        )
        
        time = round(perf_counter() - self.status, 2)
        kills = f'Убито чёрных - {16 - len(self.last[0])}\nУбито белых - {16 - len(self.last[1])}'
        points = f'Очков у чёрных - {x}\nОчков у белых - {y}'
        stop = str(datetime.now())
        write = ('Черные', 'Белые', 'Ничья')[win], self.start, stop, time, kills, points

        with CONNECTION.cursor() as cursor:
            insert_query = f'''INSERT INTO parties (winner, start_date, end_date, part_time, kills, points)
            VALUES {str(write)}'''
            cursor.execute(insert_query)
            CONNECTION.commit()
        
        self.last = ([], [])
        self.matrix = [[Void()] * 8 for _ in range(8)]

    def __repr__(self) -> str:
        return '\n'.join(' '.join(map(str, r)) for r in reversed(self.matrix))
        