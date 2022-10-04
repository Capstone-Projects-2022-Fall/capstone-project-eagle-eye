import unittest
import gui

class TestGUI(unittest.TestCase):
    """Tests all testable parts of the GUI
    
    Due to the nature of the tkinter program unit testing is limited. Anything with root.mainloop() puases execution and waits 
    for input. Because of this we can only test functionality/functions without this behavior. 
    """
    def test_mode(self):
        """Tests the mode check variable"""
        testGui = gui.App(290,200)
        testGui.mode_checked.set("Live")
        self.assertEqual(testGui.mode_checked.get(), "Live")
        testGui.mode_checked.set("Prerecorded")
        self.assertEqual(testGui.mode_checked.get(), "Prerecorded")
        pass
    def test_sport(self):
        """Tests the sport check variable"""
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
        """Tests the cleanup functionality"""
        testGui = gui.App(290,200)
        testGui.video_infile_name.set("test/file/name")
        self.assertEqual(testGui.video_infile_name.get(), "test/file/name")
        testGui.do_cleanup()
        self.assertEqual(testGui.video_infile_name.get(), "")
        pass

if __name__ == '__main__':
    unittest.main()