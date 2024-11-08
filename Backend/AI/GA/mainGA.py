import random

from AI.GA.GeneticAlgorithm import GA
from AI.utils import read_MSLatte_json, extract_activity_info, plot_fitness_evolution
from domain.Activity import Activity

def fitness_function(chromosome, problem_params):
    fitness = 0.0
    activities= problem_params['activities']
    patterns = problem_params['patterns']
    if problem_params['weekday'] == 0:
        week = "WE_"
    else:
        week = "WD_"
    representation = chromosome.representation
    for i in range(len(representation)):
        #Activity obj
        activity = activities[i]
        dataset_activ = patterns[i]
        time = representation[i][0]
        loc = representation[i][1]
        if dataset_activ != '':
            row = problem_params['data'].loc[[dataset_activ]]
            x = row[week+time].iloc[0]
            y = row[loc].iloc[0]
        else:
            x=0
            y=0
        if activity.daytime == time:
            x = 1.5
        if activity.location == loc:
            y = 1.5
        fitness = fitness + x * 0.6 + 0.3 * y + 0.1*chromosome.day_periods[time]
        chromosome.day_periods[time] -= 1
    return fitness

def run_GA(activities, ga_param, fitness_func,problem_params):
    ga = GA(fitness_func,problem_params, ga_param)
    ga.initialisation_exp1(activities)
    ga.evaluation()
    best_crom = ga.best_chromosome()

    best_fitness_history = []
    average_fitness_history = []

    for generation in range(ga_param['noGen']):
        #ga.one_generation(activities)
        ga.one_generation_elitism()
        current_best = ga.best_chromosome()
        current_average = ga.average_chromosome()
        best_fitness_history.append(current_best.fitness)
        average_fitness_history.append(current_average)
        print(str(generation + 1) + ' Current best: ' + ' \nFitness: '
              + str(current_best.fitness))
        print(current_best)

        if current_best.fitness > best_crom.fitness:
            best_crom = current_best
    plot_fitness_evolution(best_fitness_history, average_fitness_history,ga_param['popSize'],ga_param['noGen'],ga_param['mutFactor'])
    return best_crom

def generate_activ(data, no_activ,day_periods,locations):
    activities = []
    quarter = no_activ/4
    # for a quarter of the activities we will mention the daytime or location
    # we generate a random value, 0 for daytime and 1 for location
    for i in range(no_activ):
        vals = list(data.index.values)
        activ = Activity(random.choice(vals))
        if quarter > 0:
            rnd_chance = random.randint(0, 1)
            if rnd_chance == 0:
                daytime = random.choice(day_periods)
                activ.daytime = daytime
            else:
                location = random.choice(locations)
                activ.location = location
            quarter -= 1
        activities.append(activ)
    return activities

def find_patterns(activities,data):
    patterns = []
    for activity in activities:
        if activity.start_time != None :
            patterns.append('')
        else:
            match, perc = extract_activity_info(activity.label, data)
            print(activity.label + " "+ match + " "+ str(perc))
            if perc >=90:
                patterns.append(match)
            else:
                patterns.append('')
    return patterns

def test_activ():
    a1 = Activity("grocery shopping")
    a2= Activity("dinner preparation")
    a3 = Activity("homework",'Loc_Home')
    a4 = Activity("university", None, '12:45', '14:00',None,None,'morning')
    a5=Activity("gym")
    a6 = Activity("breakfast", 'Loc_Home')
    a7 = Activity("shower")
    a8 = Activity("homework", 'Loc_Home')
    a9 = Activity("homework", 'Loc_Home')
    activities = [a1,a2,a3,a4,a5]
    return activities
def main_f():
    data = read_MSLatte_json()
    ga_params = {'popSize': 30, 'noGen': 150, 'mutFactor':10, 'crossFactor':100}
    day_periods = {'morning':0, 'afternoon':0, 'evening':0, 'night':0, 'anytime':0}
    locations = ['Loc_Home', 'Loc_Public', 'Loc_Work']
    #activities = test_activ()
    activities = generate_activ(data,12,list(day_periods.keys()),locations)

    patterns = find_patterns(activities, data)
    problem_params = {'activities':activities,'patterns':patterns, 'day_periods' : day_periods, 'locations' : locations, 'weekday' : 0, 'greater_op':1, 'data':data}
    best = run_GA(activities, ga_params, fitness_function,problem_params)
    print("Input")
    print(activities)
    print("Today's activities")
    print(patterns)
    print("Final best")
    for tuple in best.representation:
        print("( " + tuple[0] +" "+ tuple[1] + " )")

main_f()