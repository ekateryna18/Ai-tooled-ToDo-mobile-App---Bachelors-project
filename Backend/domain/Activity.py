class Activity:
    def __init__(self, label, location=None, start_time=None, end_time=None, duration=None, date=None,daytime=None):
        self.__id__ = None
        self.__label__ = label
        self.__location__ = location
        self.__start_time__ = start_time
        self.__end_time__ = end_time
        self.__duration__ = duration
        self.__daytime__ = daytime
        self.__date__ = date
        self.__completed__ = False
    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self,other):
        self.__id__ = other
    @property
    def label(self):
        return self.__label__

    @property
    def location(self):
        return self.__location__

    @location.setter
    def location(self, other):
        self.__location__ = other

    @property
    def start_time(self):
        return self.__start_time__

    @property
    def end_time(self):
        return self.__end_time__

    @property
    def duration(self):
        return self.__duration__

    @property
    def daytime(self):
        return self.__daytime__

    @daytime.setter
    def daytime(self, other):
        self.__daytime__ = other
    @property
    def date(self):
        return self.__date__



    @start_time.setter
    def start_time(self, value):
        self.__start_time__ = value

    @end_time.setter
    def end_time(self, value):
        self.__end_time__ = value

    @property
    def completed(self):
        return self.__completed__

    @completed.setter
    def completed(self, value):
        self.__completed__ = value

    @duration.setter
    def duration(self, value):
        self.__duration__ = value

    def __str__(self) -> str:
        return str(self.id)+" "+ self.label + " " + str(self.daytime) + " " + str(self.location) + " "+ str(self.start_time) + " " + str(self.end_time) + " "+str(self.duration)

