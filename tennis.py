import os
from sport import Sport

class Tennis(Sport):
    """Override superclass model with the path to actual sport model"""
    @property
    def model(self):
        return os.path.join(os.getcwd(), 'models', 'tennis', 'bestSoFar_le_plus_other_model.pt')

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
    
# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

