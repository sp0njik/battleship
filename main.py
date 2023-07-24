from random import randint


class Ship:
    def __init__(self, cords: list[tuple[int, int]]):
        self.cords = cords

    def is_intersect(self, new_x, new_y):
        for x, y in self.cords:
            if abs(new_x - x) < 2 and abs(new_y - y) < 2:
                return True
        return False


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.map = ['O' * self.width for i in range(self.height)]

    def draw(self):
        map_str = '\t| ' + ' | '.join(map(str, range(self.width))) + ' |\n'
        for index, row in enumerate(self.map):
            map_str += str(index) + '\t| ' + ' | '.join(row) + ' |\n'
        return map_str


board = Board(6, 6)
ship_types_dict = {3: 1, 2: 2, 1: 4}
ships_list = []
for ship_type, count in ship_types_dict.items():
    for i in range(count):
        is_found = False
        attempts_count = 100
        while not is_found:
            if attempts_count == 0:
                ships_list.clear()
                attempts_count = 100
            x = randint(0, board.width - 1)  # column 0-5
            y = randint(0, board.height - 1)  # row 0-5
            direction = randint(1, 4)  # 1-top, 2-right, 3-bottom, 4-left
            cords = [(x, y)]
            is_found = True
            for j in range(1, ship_type):
                if direction == 1:
                    x, y = x, y - 1
                elif direction == 2:
                    x, y = x + 1, y
                elif direction == 3:
                    x, y = x, y + 1
                elif direction == 4:
                    x, y = x - 1, y
                if 0 <= x < board.width and 0 <= y < board.height:
                    cords.append((x, y))
                    is_found = True
                else:
                    is_found = False
                    attempts_count -= 1
                    break
            if not is_found:
                continue
            for x, y in cords:
                for ship in ships_list:
                    if ship.is_intersect(x, y):
                        is_found = False
                        attempts_count -= 1
                        break
        if is_found:
            ship = Ship(cords)
            ships_list.append(ship)
            print(cords, direction)

print(board.draw())
print(len(ships_list))
