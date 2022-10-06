from sport import Sport

class Tennis(Sport):
    def __init__(self, sportname):
        super().__init__(sportname)
    def printname(self):
        print(self.sportname)

tennis = Tennis('tennis')

tennis.printname()
print(tennis.model)