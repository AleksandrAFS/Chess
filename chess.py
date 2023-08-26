from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, x, y, color):
        self._x, self._y, self._color = x, y, color

    @abstractmethod
    def access_check(self):
        raise NotImplementedError
    
    @abstractmethod
    def correct(self):
        raise NotImplementedError
    

if __name__ == '__main__':
    pass