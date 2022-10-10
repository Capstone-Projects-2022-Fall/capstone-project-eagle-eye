import unittest
import os
import gui
from soccer import Soccer
from tennis import Tennis
from basketball import BasketBall

class TestSuite(unittest.TestCase):
    """Tests all testable parts of the GUI and the sport classes
    
    Due to the nature of the tkinter program unit testing is limited. Anything with root.mainloop() pauses execution and waits 
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
    def test_tennis(self):
        """Tests the sport tennis"""
        pathToModel = os.path.join(os.getcwd(), 'models', 'tennis', 'bestSoFar_le_plus_other_model.pt')
        tennis = Tennis('tennis')
        self.assertEqual(tennis.printname(), "tennis")
        self.assertEqual(tennis.model, pathToModel)
        self.assertEqual(tennis.setmodeloptions(tennis.model), f"changing model options with {pathToModel}")
        self.assertEqual(tennis.sendscript(tennis.model), pathToModel)
        pass
    def test_soccer(self):
        """Tests the sport soccer"""
        soccer = Soccer('soccer')
        self.assertEqual(soccer.printname(), "soccer")
        self.assertEqual(soccer.model, "modelofsoccer.pt")
        self.assertEqual(soccer.setmodeloptions(soccer.model),"changing model options with modelofsoccer.pt")
        self.assertEqual(soccer.sendscript(soccer.model), "modelofsoccer.pt")
        pass
    def test_basketball(self):
        """Tests the sport basketball"""
        basketball = BasketBall('basketball')
        self.assertEqual(basketball.printname(), "basketball")
        self.assertEqual(basketball.model, "modelofbasketball.pt")
        self.assertEqual(basketball.setmodeloptions(basketball.model),"changing model options with modelofbasketball.pt")
        self.assertEqual(basketball.sendscript(basketball.model), "modelofbasketball.pt")
        pass

if __name__ == '__main__':
    unittest.main()
