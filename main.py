from random import randint
from abc import ABC, abstractmethod


class Point:
    def __init__(self, x: int, y: int, marker: str):
        self.__x = x
        self.__y = y
        self.__marker = marker

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, value: str):
        if value not in ['T', 'X', '\u25fc', '\u2D54']:
            raise ValueError('wrong marker')
        self.__marker = value

    def __str__(self):
        return self.__marker


class Ship:
    def __init__(self, cords: list[Point]):
        self.__cords = cords
        for cord in self.__cords:
            cord.marker = '\u25fc'

    def is_intersect(self, new_x, new_y):
        for point in self.__cords:
            if abs(new_x - point.x) < 2 and abs(new_y - point.y) < 2:
                return True
        return False

    def is_own_point(self, x, y):
        for point in self.__cords:
            if point.x == x and point.y == y:
                return True
        return False

    def is_alive(self):
        for point in self.__cords:
            if point.marker == '\u25fc':
                return True
        return False


class Board:

    def __init__(self, width: int, height: int, ship_types_dict: dict[int, int]):
        required_cell_count = 0
        for ship_type, count in ship_types_dict.items():
            required_cell_count += (ship_type + 1) * 2 * count
        if required_cell_count > width * height:
            raise ValueError('Слишком маленький размер карты, попробуйте увеличить карту')
        self.__ship_types_dict = ship_types_dict
        self.__width = width
        self.__height = height
        self.__map: list[list[Point]] = []
        for i in range(self.__height):
            self.__map.append([])
            for j in range(self.__width):
                marker = '\u2D54'
                point = Point(i, j, marker)
                self.__map[i].append(point)
        self.__ship_list = self.__generate_ships()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def draw(self):
        map_str = '\t|\t' + '\t|\t'.join(map(str, range(1, self.__width + 1))) + '\t|\n'
        for index, row in enumerate(self.__map):
            map_str += str(index + 1) + '\t|\t' + '\t|\t'.join([str(point) for point in row]) + '\t|\n'
        return map_str

    def __get_next_point(self, direction, prev_x, prev_y):
        if direction == 1:
            x, y = prev_x - 1, prev_y
        elif direction == 2:
            x, y = prev_x, prev_y + 1
        elif direction == 3:
            x, y = prev_x + 1, prev_y
        elif direction == 4:
            x, y = prev_x, prev_y - 1
        if 0 <= x < self.__height and 0 <= y < self.__width:
            return x, y
        else:
            return None, None

    def __check_current_point_against_ships(self, x, y, ships_list):
        for ship in ships_list:
            if ship.is_intersect(x, y):
                return True
        return False

    def __generate_ships(self):
        ships_list = []
        ship_doesnt_set = True
        while ship_doesnt_set:
            ships_list.clear()
            self.clear()
            for ship_type, count in self.__ship_types_dict.items():
                for i in range(count):
                    is_found = False
                    attempts_count = 100
                    while not is_found:
                        cords = []
                        if attempts_count == 0:
                            ship_doesnt_set = True
                            break
                        x = randint(0, self.__height - 1)  # column 0-5
                        y = randint(0, self.__width - 1)  # row 0-5
                        direction = randint(1, 4)  # 1-top, 2-right, 3-bottom, 4-left
                        if self.__check_current_point_against_ships(x, y, ships_list):
                            is_found = False
                            attempts_count -= 1
                            continue
                        cords = [self.__map[x][y]]
                        is_found = True
                        for i in range(1, ship_type):
                            x, y = self.__get_next_point(direction, x, y)
                            if (x == None and y == None) or self.__check_current_point_against_ships(x, y, ships_list):
                                is_found = False
                                attempts_count -= 1
                                break
                            else:
                                cords.append(self.__map[x][y])
                                is_found = True
                            # if not is_found:
                            #     continue

                    if is_found:
                        ship = Ship(cords)
                        ships_list.append(ship)
                        # print(cords, direction)
                        ship_doesnt_set = False
                    if ship_doesnt_set:
                        break
                if ship_doesnt_set:
                    break
            else:
                ship_doesnt_set = False

        return ships_list

    def check_point(self, x: int, y: int) -> str:
        if self.__map[x][y].marker in ['X', 'T']:
            raise ValueError('You already have been shot at this coords')
        for ship in self.__ship_list:
            if ship.is_own_point(x, y):
                marker = 'X'
                break
        else:
            marker = 'T'
        self.__map[x][y].marker = marker
        return marker

    def set_marker(self, x: int, y: int, marker: str):
        self.__map[x][y].marker = marker

    def is_any_ships(self):
        for ship in self.__ship_list:
            if ship.is_alive():
                return True
        return False

    def clear(self):
        for row in self.__map:
            for point in row:
                point.marker = '\u2D54'


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


if __name__ == '__main__':
    ship_types_dict = {3: 1, 2: 2, 1: 4}
    user = User('Artak', 6, 6, ship_types_dict)
    ai = Ai('Computer', 6, 6, ship_types_dict)
    user.set_opponent(ai)
    ai.set_opponent(user)
    active_player = user
    while True:
        print(f'Ход, {active_player.name}')
        print(active_player.draw_boards())
        shoot = active_player.shoot()
        if not active_player.is_winner():
            if shoot == 'T' and active_player is user:
                active_player = ai
            elif shoot == 'T' and active_player is ai:
                active_player = user
        else:
            print(f'Победитель: {active_player.name}')
            break
        print(f'Результат выстрела {active_player.name}')
        print(active_player.draw_boards())

    # ship_types_dict = {3: 1, 2: 2, 1: 4}
    # while True:
    #     width = int(input('Enter the width: '))
    #     height = int(input('Enter the height: '))
    #     try:
    #         board = Board(width, height, ship_types_dict)
    #         break
    #     except ValueError as error:
    #         print(error)
    #
    # print(board.draw())
