from itertools import product
from figures import King, Knight, Bishop, Queen, Pawn, Rook, Void, Figure
from time import perf_counter
import pymysql
from connectSQL import host, db_name, password, user
from datetime import datetime, timedelta


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

    __result: dict = {
        Pawn: 1, Knight: 2, Rook: 3,
        Bishop: 3, King: 0, Queen: 5
    }

    def __init__(self) -> None:
        self.matrix = [[Void()] * 8 for _ in range(8)]
        self.types = (Rook, Knight, Bishop)
        self.all_figures = ([], [])
        self.kinges, self.status = [], perf_counter()
        self.start = str(datetime.now())

        self.create(1, True)
        self.create(7, False)

        self.end()

    def __getitem__(self, index: int):
        return self.matrix[index]

    def create(self, side: int, color: bool) -> None:

        # установка пешек

        for value in range(8):
            pawn = Pawn(color, self.matrix)
            self.matrix[side][value] = pawn
            pawn.qn = self.all_figures[color]

        # устанока экземпляров классов из кортежа self.types

        for key in range(3):
            self.matrix[side - 1][key] = self.types[key](color, self.matrix)
            self.matrix[side - 1][~key] = self.types[key](color, self.matrix)

         # установка короля и королевы

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
                obj.enemy_figures = self.all_figures[not obj._color]
                self.all_figures[obj._color].append(obj)
                obj.your_king = self.kinges[not obj._color]
                obj.enemy_king = self.kinges[obj._color]
                obj.your_board = self

    def surrender(self, *, determine_winner: bool = True) -> None:
        """Запись в SQL базу данных результата поединка и 
        удаление данных о фигурах и таблице"""

        x = sum(self.__result[i.__class__] for i in self.all_figures[0])
        y = sum(self.__result[i.__class__] for i in self.all_figures[1])

        win = (
            not Figure._whose_move
            if determine_winner else
            (x > y, x < y, x == y).index(True)
        ) if isinstance(determine_winner, bool) else determine_winner

        time = str(timedelta(seconds=round(perf_counter() - self.status)))
        kills = f'Убито чёрных - {16 - len(self.all_figures[0])}\nУбито белых - {16 - len(self.all_figures[1])}'
        points = f'Очков у чёрных - {x}\nОчков у белых - {y}'
        stop = str(datetime.now())
        write = ('Черные', 'Белые', 'Ничья')[win], self.start, stop, time, kills, points

        with CONNECTION.cursor() as cursor:
            try:
                cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")
                cursor.execute("START TRANSACTION;")
                insert_query = f'''INSERT INTO parties (winner, start_date, end_date, part_time, kills, points)\
                                   VALUES {str(write)};'''
                cursor.execute(insert_query)
                CONNECTION.commit()
            except Exception as e:
                CONNECTION.rollback()
                print(e)

        self.all_figures = ([], [])
        self.matrix = [[Void()] * 8 for _ in range(8)]

    def __repr__(self) -> str:
        return '\n'.join(' '.join(map(str, r)) for r in reversed(self.matrix))
