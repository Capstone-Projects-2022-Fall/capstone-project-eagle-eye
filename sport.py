from abc import ABC, abstractmethod
class Sport(ABC):
    def __init__(self, sportname):
        self.sportname = sportname

    @property
    def model(self):
        return f"model of {self.sportname}.pt"

    @abstractmethod
    def printname(self):
        pass
