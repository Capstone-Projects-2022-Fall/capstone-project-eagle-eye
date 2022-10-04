import unittest
import gui

# testGui = gui.App()

# testGui.__init__(290,200)
# testGui.mode_checked = "Live"
# testGui.enter()


class TestGUI(unittest.TestCase):

    def test_mode(self):
        testGui = gui.App(290,200)
        testGui.mode_checked.set("Live")
        self.assertEqual(testGui.mode_checked.get(), "Live")
        testGui.mode_checked.set("Prerecorded")
        self.assertEqual(testGui.mode_checked.get(), "Prerecorded")
        pass
    def test_sport(self):
        testGui = gui.App(290,200)
        testGui.sport_checked.set("Tennis")
        self.assertEqual(testGui.sport_checked.get(), "Tennis")
        testGui.sport_checked.set("Soccer")
        self.assertEqual(testGui.sport_checked.get(), "Soccer")
        testGui.sport_checked.set("Basketball")
        self.assertEqual(testGui.sport_checked.get(), "Basketball")
        testGui.sport_checked.set("Baseball")
        self.assertEqual(testGui.sport_checked.get(), "Baseball")
        testGui.sport_checked.set("Hockey")
        self.assertEqual(testGui.sport_checked.get(), "Hockey")
        testGui.sport_checked.set("Ping Pong")
        self.assertEqual(testGui.sport_checked.get(), "Ping Pong")
        pass
    def test_cleanup(self):
        testGui = gui.App(290,200)
        testGui.video_infile_name.set("test/file/name")
        self.assertEqual(testGui.video_infile_name.get(), "test/file/name")
        testGui.do_cleanup()
        self.assertEqual(testGui.video_infile_name.get(), "")
    def test_error(self):
        testGui = gui.App(290,200)
        testGui.error_message(error="this is an error message")
        testGui.stop()
        pass

if __name__ == '__main__':
    unittest.main()