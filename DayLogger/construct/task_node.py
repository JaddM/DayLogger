# Author Jadd, Nov 8 2020
# To create a class which organizes the task data and implements methods for ease of collection

class TaskNode:

    def __init__(self, identification, start_time, end_time, perspective, category, description):

        self.__identification = identification
        self.__start_time = start_time
        self.__end_time = end_time
        self.__perspective = perspective
        self.__category = category
        self.__description = description

        if category == "PRODUCTIVE": self.__colour = 'green'
        elif category == "LEISURE": self.__colour = 'red'
        elif category == "SLEEP": self.__colour = 'blue'

    def get_id(self): return self.__identification

    def get_start_time(self): return self.__start_time

    def get_end_time(self): return self.__end_time

    def get_duration(self):
        start = self.get_start_time()
        end = self.get_end_time()

        if start % 100 != 0: start += 20
        if end % 100 != 0: end += 20

        return end/100 - start/100

    def get_perspective(self): return self.__perspective
    def get_category(self): return self.__category
    def get_description(self): return self.__description
    def get_colour(self): return self.__colour
