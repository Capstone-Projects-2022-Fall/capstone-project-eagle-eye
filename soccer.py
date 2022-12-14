import os
import sys
from sport import Sport

class Soccer(Sport):
    # for later use, remember to change path
    # """Override superclass model with the path to actual sport model"""
    @property
    def model(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        relative_path = os.path.join('models', 'soccer', 'soccer_model4.pt')
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    def __init__(self, sportname):
        super().__init__(sportname)

    def printname(self):
        return self.sportname
    
    def setmodeloptions(self,model):
        return f"changing model options with {model}"

    def setfieldoptions(self,field):
        return f"changing field options with {field}"

    def sendscript(self, model):
        return model
# soccer = Soccer('soccer')

# soccer.printname()
# print(soccer.model)
# soccer.setmodeloptions(soccer.model)
# print(soccer.field)
# soccer.setfieldoptions(soccer.field)

