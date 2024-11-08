import random

class MyChromosome:
    def __init__(self):
        self.__day_periods = {'morning':0, 'afternoon':0, 'evening':0, 'night':0, 'anytime':0}
        self.__locations = ['Loc_Home', 'Loc_Public', 'Loc_Work']
        self.__weekday = 0
        self.__fitness=0.0
        self.__representation = []

    @property
    def representation(self):
        return self.__representation

    @property
    def fitness(self):
        return self.__fitness

    @property
    def weekday(self):
        return self.__weekday

    @property
    def day_periods(self):
        return self.__day_periods

    @representation.setter
    def representation(self, chromosome_rep):
        self.__representation = chromosome_rep

    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    def crossover(self, other):

        cut = random.randint(0, len(self.__representation)-1)
        new_repr = [None] * len(self.__representation)
        for i in range(cut):
            new_repr[i] = self.__representation[i]
        for i in range(cut, len(self.__representation)):
            new_repr[i] = other.__representation[i]
        offspring = MyChromosome()
        offspring.__representation = new_repr
        return offspring

    def mutation(self, mutation_rate):

        rnd_chance = random.randint(0,100)
        if rnd_chance < mutation_rate:
            poz_1 = random.randint(0, len(self.__representation)-1)
            poz_2 = random.randint(0, len(self.__representation)-1)
            self.__representation[poz_1], self.__representation[poz_2] = \
                self.__representation[poz_2], self.__representation[poz_1]

    def init_representation(self,activities):
        '''
        Cromozom sub forma de tupluri (ActivityId, Daytime, Location)
        ActivityId - index activity in activities
        :param activities: String of activities split by ','
        :return:
        '''
        day_periods = list(self.__day_periods.keys())
        possible_daytimes = len(day_periods)-1
        possible_locations = len(self.__locations)-1
        for i in range(len(activities)):
            daytime = day_periods[random.randint(0,possible_daytimes)]
            if activities[i].location:
                location = activities[i].location
            else:
                location = self.__locations[random.randint(0,possible_locations)]
            self.__representation.append((daytime,location))

    def __str__(self) -> str:
        repr = ""
        for tuple in self.__representation:
            tup = ""
            for t in tuple:
                tup += str(t)
                tup += " "
            repr = repr + " ( " + tup + " ) "
        return "\nChromosome" + repr + "---fit:  " + str(self.__fitness)

