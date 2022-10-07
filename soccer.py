from sport import Sport

class Soccer(Sport):
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
soccer = Soccer('soccer')

soccer.printname()
print(soccer.model)
soccer.setmodeloptions(soccer.model)
print(soccer.field)
soccer.setfieldoptions(soccer.field)

