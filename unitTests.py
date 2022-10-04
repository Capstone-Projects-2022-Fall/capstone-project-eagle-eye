import unittest
import gui

# gui1 = gui.App()

# gui1.__init__(290,200)
# gui1.mode_checked = "Live"
# gui1.enter()


class TestUser(unittest.TestCase):

    def test_mode(self):
        gui1 = gui.App(290,200)
        gui1.mode_checked.set("Live")
        self.assertEqual(gui1.mode_checked.get(), "Live")
        gui1.mode_checked.set("Prerecorded")
        self.assertEqual(gui1.mode_checked.get(), "Prerecorded")
        pass
    def test_sport(self):
        gui1 = gui.App(290,200)
        gui1.sport_checked.set("Tennis")
        self.assertEqual(gui1.sport_checked.get(), "Tennis")
        gui1.sport_checked.set("Soccer")
        self.assertEqual(gui1.sport_checked.get(), "Soccer")
        gui1.sport_checked.set("Basketball")
        self.assertEqual(gui1.sport_checked.get(), "Basketball")
        gui1.sport_checked.set("Baseball")
        self.assertEqual(gui1.sport_checked.get(), "Baseball")
        gui1.sport_checked.set("Hockey")
        self.assertEqual(gui1.sport_checked.get(), "Hockey")
        gui1.sport_checked.set("Ping Pong")
        self.assertEqual(gui1.sport_checked.get(), "Ping Pong")
        pass

if __name__ == '__main__':
    unittest.main()