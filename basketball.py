import os
from sport import Sport

class BasketBall(Sport):
    # for later use, remember to change path
    # """Override superclass model with the path to actual sport model"""
    # @property
    def model(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        relative_path = os.path.join('models', 'basketball', 'basketball.pt')
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        print(os.path.join(base_path, relative_path))
        return os.path.join(base_path, relative_path)
        print(os.getcwd())
        print(os.path.join(os.getcwd(), 'models', 'basketball', 'basketball.pt'))
        return os.path.join(os.getcwd(), 'models', 'basketball', 'basketball.pt')

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

# basketball = BasketBall('basketball')

# basketball.printname()
# print(basketball.model)
# basketball.setmodeloptions(basketball.model)
# print(basketball.field)
# basketball.setfieldoptions(basketball.field)

