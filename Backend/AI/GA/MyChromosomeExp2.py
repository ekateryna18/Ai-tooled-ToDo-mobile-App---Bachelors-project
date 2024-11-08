import random
from random import randint
class MyChromosomeExp2:
    def __init__(self):
        self.__fitness=0.0
        self.__fixed = False
        self.__representation = []

    @property
    def representation(self):
        return self.__representation

    @property
    def fixed(self):
        return self.__fixed
    @property
    def fitness(self):
        return self.__fitness

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
        offspring = MyChromosomeExp2()
        offspring.__representation = new_repr
        return offspring

    def mutation(self, mutation_rate):
        rnd_chance = randint(0,100)
        if rnd_chance < mutation_rate:
            poz_1 = randint(0, len(self.__representation)-1)
            poz_2 =randint(0, len(self.__representation)-1)
            self.__representation[poz_1], self.__representation[poz_2] = \
                self.__representation[poz_2], self.__representation[poz_1]

    def init_representation(self, activities, dataset, current_time):
        '''
        Chromosome in tuple format (ActivityId, StartTime, Duration)
        ActivityId - index activity in activities
        :param weekday: the day of the week, int
        :param activities: list of activities
        :param dataset: the dataset just with data from the same weekday to initialise cromozomes mimicing past schedules
        :return:
        '''

        for i in range(len(activities)):
            start_time = 0
            duration = 0
            # if activities[i].start_time is not None:
            #     start_time = activities[i].start_time
            print(str(activities[i]['label']) + " " + str(activities[i]['duration']))
            #if int(activities[i]['duration']) != 0 and activities[i]['duration'] is not None :
            if activities[i]['fixed_by_user'] is True:
                duration = activities[i]['duration']
                start_time = activities[i]['start_time']
                self.__fixed = True
            #if start_time == 0 or duration == 0:
            if duration == 0:
                #get a random date from the dataset
                date = dataset['date'].sample().iloc[0]
                # all the rows from the date
                data = dataset[dataset['date'] == date]
                if data['activity'].isin([activities[i]['label']]).any() == True:
                    activity = data[data['activity'] == activities[i]['label']].sample()
                    #activity = data[(data['activity'] == activities[i].label) & (data['start_time'] >= current_time)].sample()
                    # if start_time is None:
                    #     start_time = activity['start_time'].iloc[0]
                    if duration == 0:
                        duration = activity['time'].iloc[0]
                else:
                    #duration maximum 8 hours since sleep is longest
                    duration = random.randint(0,480)
                #start_time = random.randint(current_time,1439)
                start_time = random.randint(670,1439)
            self.__representation.append((start_time,duration))

    def __str__(self) -> str:
        repr = ""
        for tuple in self.__representation:
            tup = ""
            for t in tuple:
                tup += str(t)
                tup += " "
            repr = repr + " ( " + tup + " ) "
        return "\nChromosome" + repr + "---fit:  " + str(self.__fitness)

