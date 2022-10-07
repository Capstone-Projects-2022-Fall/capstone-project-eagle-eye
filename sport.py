from abc import ABC, abstractmethod
class Sport(ABC):
    """Abstract class for available sports and their models.
    
    Each sport will have a model and field property
    """
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
        """For only test purpose. Will print the name of the sport"""
        pass
    
    @abstractmethod
    def setmodeloptions(model):
        """Will change any needed options or arguments needed for the dectect script to run
            Args:
            model: the model that will be used
            """
        pass
    @abstractmethod
    def setfieldoptions(model):
        """Will change any needed options or arguments needed for the field of the sport
            Args:
            field: the field that will be used
            """
        pass

    @abstractmethod
    def sendscript(model):
        """Will send to the sport selector the updated script for dectect.py
            Args:
            model: the model that will be used
            """
        pass