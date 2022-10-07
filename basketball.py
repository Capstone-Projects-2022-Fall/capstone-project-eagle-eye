from sport import Sport

class BasketBall(Sport):
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

basketball = BasketBall('basketball')

basketball.printname()
print(basketball.model)
basketball.setmodeloptions(basketball.model)
print(basketball.field)
basketball.setfieldoptions(basketball.field)

