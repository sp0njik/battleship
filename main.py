from players import Ai, User

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
