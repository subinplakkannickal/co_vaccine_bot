from abc import ABC, abstractmethod

class AbstractSlotSearch(ABC):

    @abstractmethod
    def get_vaccine_slots(self):
        pass

    @abstractmethod
    def get_user_inputs(self):
        pass