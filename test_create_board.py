from unittest import TestCase
from main import Board


class CreateBoard(TestCase):
    def test_create_board_fail(self):
        with self.assertRaises(ValueError):
            board = Board(3, 3, {3: 1, 2: 2, 1: 4})

    def test_create_board_success(self):
        try:
            board = Board(6, 6, {3: 1, 2: 2, 1: 4})
        except ValueError:
            self.fail('wrong data for creating board')


# if __name__ == '__main__':
#     main()
