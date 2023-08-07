from random import randint
from abc import ABC, abstractmethod


class Ship:
    def __init__(self, cords: list[tuple[int, int]]):
        self.__cords = cords

    def is_intersect(self, new_x, new_y):
        for x, y in self.__cords:
            if abs(new_x - x) < 2 and abs(new_y - y) < 2:
                return True
        return False

    def is_own_point(self, x, y):
        return (x, y) in self.__cords


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
        self.__ship_list = self.__generate_ships()
        self.__map = []
        for i in range(self.__height):
            self.__map.append([])
            for j in range(self.__width):
                marker = '\u2D54'
                for ship in self.__ship_list:
                    if ship.is_own_point(i, j):
                        marker = '\u25fc'
                        break
                self.__map[i].append(marker)

    def draw(self):
        map_str = '\t|\t' + '\t|\t'.join(map(str, range(self.__width))) + '\t|\n'
        for index, row in enumerate(self.__map):
            map_str += str(index) + '\t|\t' + '\t|\t'.join(row) + '\t|\n'
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
            for ship_type, count in self.__ship_types_dict.items():
                for i in range(count):
                    is_found = False
                    attempts_count = 100
                    while not is_found:
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
                        cords = [(x, y)]
                        is_found = True
                        for i in range(1, ship_type):
                            x, y = self.__get_next_point(direction, x, y)
                            if (x == None and y == None) or self.__check_current_point_against_ships(x, y, ships_list):
                                is_found = False
                                attempts_count -= 1
                                break
                            else:
                                cords.append((x, y))
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
        if self.__map[x][y] in ['X', 'T']:
            raise ValueError('You already have been shot at this coords')
        for ship in self.__ship_list:
            if ship.is_own_point(x, y):
                marker = 'X'
                break
        else:
            marker = 'T'
        self.__map[x][y] = marker
        return marker

    def set_marker(self, x: int, y: int, marker: str):
        self.__map[x][y] = marker


class Player:
    def __init__(self, name: str, width: int, height: int, ships_type_dict: dict[int, int]):
        self.name = name
        self.__own_board = Board(width, height, ships_type_dict)
        self.__opponent_board = Board(width, height, {})

    def shoot(self):
        while True:
            try:
                x, y = self.get_cords()
                marker = self.__opponent.check_shoot(x, y)
                break
            except ValueError as error:
                print(error)
        self.__opponent_board.set_marker(x, y, marker)

    def get_cords(self) -> tuple[int, int]:
        pass

    def set_opponent(self, opponent):
        self.__opponent: Player = opponent

    def check_shoot(self, x: int, y: int) -> str:
        return self.__own_board.check_point(x, y)


if __name__ == '__main__':

    ship_types_dict = {3: 1, 2: 2, 1: 4}
    while True:
        width = int(input('Enter the width: '))
        height = int(input('Enter the height: '))
        try:
            board = Board(width, height, ship_types_dict)
            break
        except ValueError as error:
            print(error)

    print(board.draw())
# написать тест на проверку создание карты слишком маленькой
# написать класс игрока Player: def get_cords(), def check_points_on_the_board(), def shoot(), init 2 доски, 1-я с заполненым перечнем, 2-я заполненная
