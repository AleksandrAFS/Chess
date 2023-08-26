from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, x: int, y: int, color: str):
        self._x, self._y, self._color = x, y, color

    @abstractmethod
    def access_check(self):
        raise NotImplementedError
    
    @abstractmethod
    def correct(self):
        raise NotImplementedError
    

class Elephant(Figure):
    def access_check(self, x: int, y: int) -> bool:
        return abs(self._x - x) == abs(self._y - y)

    def correct(self):
        pass
    

if __name__ == '__main__':
    pass