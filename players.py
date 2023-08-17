from abc import ABC, abstractmethod
from board import Board

class Player(ABC):
    def __init__(self, name: str, width: int, height: int, ships_type_dict: dict[int, int]):
        self.name = name
        self._own_board = Board(width, height, ships_type_dict)
        self._opponent_board = Board(width, height, {})
        self._opponent = None

    def shoot(self):
        while True:
            try:
                x, y = self.get_cords()
                x -= 1
                y -= 1
                marker = self._opponent.check_shoot(x, y)
                break
            except ValueError as error:
                print(error)
        self._opponent_board.set_marker(x, y, marker)
        return marker

    @abstractmethod
    def get_cords(self) -> tuple[int, int]:
        pass

    def set_opponent(self, opponent):
        self._opponent: Player = opponent

    def check_shoot(self, x: int, y: int) -> str:
        return self._own_board.check_point(x, y)

    def draw_boards(self):
        boards_str = self._own_board.draw()
        boards_str += '\n\n'
        boards_str += self._opponent_board.draw()
        return boards_str

    def has_any_ships(self):
        return self._own_board.is_any_ships()

    def is_winner(self):
        return not self._opponent.has_any_ships()


class User(Player):
    def get_cords(self) -> tuple[int, int]:
        while True:
            try:
                x, y = list(map(int, input('Введите координаты через пробел: ').split()))
                break
            except TypeError:
                print('Введены некорректные координаты, попробуйте снова')
        return x, y


class Ai(Player):
    def get_cords(self) -> tuple[int, int]:
        x = randint(1, self._own_board.width)
        y = randint(1, self._own_board.height)
        print(f'Координаты выстрела компьютера {x} {y}')
        return x, y
