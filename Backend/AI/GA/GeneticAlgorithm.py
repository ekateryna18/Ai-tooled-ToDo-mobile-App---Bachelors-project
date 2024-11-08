from random import randint, random

from AI.GA.MyChromosome import MyChromosome
from AI.GA.MyChromosomeExp2 import MyChromosomeExp2
class GA:
    def __init__(self, fitness_func,problem_params, param=None):
        self.__param = param
        self.__fitness_function = fitness_func
        self.__problem_params = problem_params
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation_exp1(self, activities):
        for _ in range(0, self.__param['popSize']):
            c = MyChromosome()
            c.init_representation(activities)
            self.__population.append(c)
    def initialisation_exp2(self, activities, data,current_time):
        for _ in range(0, self.__param['popSize']):
            c = MyChromosomeExp2()
            c.init_representation(activities, data,current_time)
            self.__population.append(c)

    def evaluation(self):
        for crom in self.__population:
            crom.fitness = self.__fitness_function(crom, self.__problem_params)

    def best_chromosome(self):
        bestc = self.__population[0]
        for crom in self.__population:
            response = self.compare_fitness(crom.fitness,bestc.fitness)
            if response is True:
                bestc = crom
        return bestc

    def average_chromosome(self):
        sum = 0
        length = len(self.__population)
        for crom in self.__population:
            sum += crom.fitness
        return sum/length
    def selection(self):
        #select from 50% fittest generation
        half_pop = int((50 * self.__param['popSize'])/100)
        pos_1 = randint(0,half_pop)
        pos_2 = randint(0, half_pop)
        if self.compare_fitness(self.__population[pos_1].fitness,self.__population[pos_2].fitness):
            return pos_1
        else:
            return pos_2

    def one_generation(self):
        new_population = []
        self.__population = sorted(self.__population, key=lambda x : x.fitness, reverse=True)
        for _ in range(self.__param['popSize']):
            crom_1 = self.__population[self.selection()]
            crom_2 = self.__population[self.selection()]
            rnd_chance = randint(0, 100)
            if rnd_chance < self.__param['crossFactor']:
                off = crom_1.crossover(crom_2)
            else:
                if self.compare_fitness(crom_1.fitness,crom_2.fitness):
                   off =  crom_1
                else:
                   off =  crom_2
            off.mutation(self.__param['mutFactor'])
            new_population.append(off)
        self.__population = new_population
        self.evaluation()

    def one_generation_elitism(self):
        reverse = True
        if self.__problem_params['greater_op'] == 0:
            reverse = False
        self.__population = sorted(self.__population, key=lambda x : x.fitness, reverse=reverse)
        #newPop = [self.best_chromosome()]
        newPop = []
        # 10% of the fittest go to the next generation
        s = int((10* self.__param['popSize'])/100)
        newPop.extend(self.__population[:s])
        s = int((90 * self.__param['popSize']) / 100)
        for _ in range(s - 1):
            crom_1 = self.__population[self.selection()]
            crom_2 = self.__population[self.selection()]
            if self.__problem_params['greater_op'] == 0 and crom_1.fixed is False and crom_2.fixed is False:
            #off = crom_1.crossover(crom_2)
                rnd_chance = randint(0, 100)
                if rnd_chance < self.__param['crossFactor']:
                    off = crom_1.crossover(crom_2)
                else:
                    if self.compare_fitness(crom_1.fitness, crom_2.fitness):
                        off = crom_1
                    else:
                        off = crom_2
                off.mutation(self.__param['mutFactor'])
            elif self.compare_fitness(crom_1.fitness,crom_2.fitness):
               off =  crom_1
            else:
               off =  crom_2

            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def compare_fitness(self,fit1,fit2):
        if self.__problem_params['greater_op'] == 0:
            if fit1 < fit2:
                return True
            else:
                return False
        elif self.__problem_params['greater_op'] == 1:
            if fit1 > fit2:
                return True
            else:
                return False