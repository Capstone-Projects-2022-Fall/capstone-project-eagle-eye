from abc import ABC, abstractmethod
class Sport(ABC):
    def __init__(self, sportname):
        self.sportname = sportname

    @property
    def model(self):
        return f"modelof{self.sportname}.pt"
    @property
    def field(self):
        return f"fieldof{self.sportname}.pt"
    @abstractmethod
    def printname(self):
        pass
    
    @abstractmethod
    def setmodeloptions(model):
        pass
    @abstractmethod
    def setfieldoptions(model):
        pass

    @abstractmethod
    def sendscript(model):
        pass