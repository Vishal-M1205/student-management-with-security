from abc import ABC, abstractmethod


class ClassInterface(ABC):

    @abstractmethod
    async def get_top_five_students(self):
        pass

    @abstractmethod
    async def get_top_five_average(self):
        pass
