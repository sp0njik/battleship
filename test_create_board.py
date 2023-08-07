from unittest import TestCase, main
from main import Board, Ship


#
#
class CreateBoard(TestCase):
    def test_create_board_fail(self):
        with self.assertRaises(ValueError):
            board = Board(3, 3, {3: 1, 2: 2, 1: 4})

    def test_create_board_success(self):
        try:
            board = Board(6, 6, {3: 1, 2: 2, 1: 4})
        except ValueError:
            self.fail('wrong data for creating board')
#
#


# from unittest import TestCase
# from main import Ship
#
#
class CheckShipTestCase(TestCase):

    def test_intersect(self):
        ship = Ship([(3, 2), (3, 3)])
        self.assertTrue(ship.is_intersect(2, 4))

    def test_false_intersect(self):
        ship = Ship([(3, 2), (3, 3)])
        self.assertFalse(ship.is_intersect(0, 5))


if __name__ == '__main__':
    main()
