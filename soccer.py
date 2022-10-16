import os
from sport import Sport

class Soccer(Sport):
    # for later use, remember to change path
    # """Override superclass model with the path to actual sport model"""
    # @property
    # def model(self):
    #     return os.path.join(os.getcwd(), 'models', 'tennis', 'bestSoFar_le_plus_other_model.pt')
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

