from AI.GA.GeneticAlgorithm import GA
from AI.GA.MyChromosomeExp2 import MyChromosomeExp2
from AI.utils import read_LifeTracking_csv, read_lifeTracking_data_analysis, plot_fitness_evolution
from domain.Activity import Activity

class MainGA:
    def __init__(self):
        self.__dataset__ = read_LifeTracking_csv()
        self.__data_analysis__ = read_lifeTracking_data_analysis()
        self.__ga_params__ = {'popSize': 35, 'noGen': 50, 'mutFactor': 10, 'crossFactor': 100}
        #self.__ga_params__ = {'popSize': 20, 'noGen': 50, 'mutFactor': 10, 'crossFactor': 100}

    def run_GA(self,activities, ga_param, fitness_func, data,problem_params):
        ga = GA(fitness_func,problem_params, ga_param)
        ga.initialisation_exp2(activities, data, problem_params['current_time'])
        ga.evaluation()
        best_crom = ga.best_chromosome()
        best_fitness_history = []
        average_fitness_history = []

        for generation in range(ga_param['noGen']):
            #ga.one_generation()
            ga.one_generation_elitism()
            current_best = ga.best_chromosome()
            current_average = ga.average_chromosome()
            best_fitness_history.append(current_best.fitness)
            average_fitness_history.append(current_average)
            print(str(generation + 1) + ' Current best: ' + ' \nFitness: '
                  + str(current_best.fitness))
            #print(current_best)
            if current_best.fitness < best_crom.fitness:
                best_crom = current_best
            print("Best: " + str(best_crom.fitness))
        plot_fitness_evolution(best_fitness_history, average_fitness_history, ga_param['popSize'],ga_param['noGen'], ga_param['mutFactor'],ga_param['crossFactor'])

        return best_crom

    def main_GA(self,weekday, activities, current_time):
        data_analysis = self.__data_analysis__[self.__data_analysis__['weekday'] == weekday]
        problem_params = {'activities': activities, 'greater_op':0, 'data_analysis': data_analysis, 'current_time': 840}
        #problem_params = {'activities': activities, 'greater_op':0, 'data_analysis': data_analysis, 'current_time': current_time}
        dataset = self.__dataset__[self.__dataset__['weekday'] == weekday]
        best = self.run_GA(activities, self.__ga_params__, self.fitness_function, dataset, problem_params)


        print("Input")
        print(activities)
        print("Final best")
        for tuple in best.representation:
            print("( " + str(tuple[0]) + " " + str(tuple[1]) + " ) fitness: " + str(best.fitness) )
        return best.representation

    def fitness_function(self,chromosome, problem_params):
        fitness = 0.0
        sorted_representation = chromosome.representation.copy()
        sorted_representation.sort(key = lambda tuple: tuple[0])
        for i in range(len(sorted_representation)):
            if i > 0:
                prev_endtime = sorted_representation[i-1][0] + sorted_representation[i-1][1]
                time_gap = sorted_representation[i][0] - prev_endtime
                if time_gap < 0 :
                    # 12 hours penalty when overriding
                    time_gap = 12*60
                    #time_gap = (-1)*time_gap
                fitness += time_gap
            start_time = chromosome.representation[i][0]
            if start_time <= problem_params['current_time']:
                #penalty one hour
                fitness += 12*60
            activ_label = problem_params['activities'][i]['label']
            analysis_df = problem_params['data_analysis']
            activity = analysis_df[analysis_df['activity'] == activ_label]
            if activity.empty is False:
                if 0 <= start_time < 360:
                    fitness -= activity['0-360'].iloc[0]
                elif 360 <= start_time < 720:
                    fitness -= activity['360-720'].iloc[0]
                elif 720 <= start_time < 1080:
                    fitness -= activity['720-1080'].iloc[0]
                elif 1080 <= start_time <= 1440:
                    fitness -= activity['1080-1440'].iloc[0]
        return fitness


