from sport import Sport

class Tennis(Sport):
    def __init__(self, sportname):
        super().__init__(sportname)

    def printname(self):
        print(self.sportname)
    
    def setmodeloptions(self,model):
        print(f"changing model options with {model}")

    def setfieldoptions(self,field):
        print(f"changing field options with {field}")
        
    def sendscript(self, model):
        return model
    
# tennis = Tennis('tennis')

# tennis.printname()
# print(tennis.model)
# tennis.setmodeloptions(tennis.model)
# print(tennis.field)
# tennis.setfieldoptions(tennis.field)

