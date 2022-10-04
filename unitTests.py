import unittest
import gui

# gui1 = gui.App()

# gui1.__init__(290,200)
# gui1.mode_checked = "Live"
# gui1.enter()


class TestUser(unittest.TestCase):

    def test_user_activation(self):
        gui1 = gui.App(290,200)
        # gui1.__init__(290,200)
        gui1.mode_checked = "Live"
        gui1.enter()
        pass

    def test_user_points_update(self):
        pass

    def test_user_level_change(self):
        pass

if __name__ == '__main__':
    unittest.main()