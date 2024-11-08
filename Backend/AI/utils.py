import pandas as pd
from thefuzz import fuzz
from fuzzywuzzy import process
import matplotlib.pyplot as plt
import numpy as np

from AI.data_processing import get_file_path


def read_MSLatte_json():
    #file = get_file_path('data_files\MsLatte_dataset\processed_data_mslatte.json')
    file = 'D:\\USB_D\\Licenta\\DailyActivBackend\\AI\\data_files\\MsLatte_dataset\\processed_data_mslatte.json'
    data = pd.read_json(file, lines=True)
    data = data.set_index('TaskTitle')
    data.drop("ID", axis=1, inplace=True)
    print("yupi")
    return data

def read_LifeTracking_csv():
    file = 'D:\\USB_D\\Licenta\\DailyActivBackend\\AI\\data_files\\LifeTracking\\csv\\processed_life_data.csv'
    data = pd.read_csv(file)
    return data

def read_lifeTracking_data_analysis():
    file = 'D:\\USB_D\\Licenta\\DailyActivBackend\\AI\\data_files\\LifeTracking\\csv\\productivity_data_analysis.csv'
    data = pd.read_csv(file)
    return data
def plot_fitness_evolution(best_fitnesses, average_fitnesess,popsize, noGen, mutfactor, crossover = 100):
    plt.figure(figsize=(12, 6))
    plt.plot(best_fitnesses, label='Best Fitness', color='red', linewidth=2)
    plt.plot(average_fitnesess, label='Average Fitness',color='blue', linestyle='--', linewidth=2)
    text = 'Population size: '+ str(popsize) + ', Generations: '+ str(noGen)  + ', Mutation factor: '+ str(mutfactor/100) + ', Crossover factor: ' + str(crossover/100)

    plt.title('Fitness Evolution Over Generations\n' + text )
    #plt.text(80, 1, text, fontsize=12, color='black')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_analysed_data_lifeTracking():
    file = get_file_path('data_files\LifeTracking\csv\productivity_data_analysis.csv')
    df = pd.read_csv(file)
    activities = df['activity'].unique()
    weekdays = df['weekday'].unique()
    n_weekdays = len(weekdays)

    # Set the width of each bar and create the figure
    bar_width = 0.8 / len(activities)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot bars for each activity
    for i, activity in enumerate(activities):
        subset = df[df['activity'] == activity]
        ax.bar(subset['weekday'] + i * bar_width, subset['average_frequency'], width=bar_width, label=activity)

    # Set the labels and title
    ax.set_xlabel('Ziua săptămânii')
    ax.set_ylabel('Frecvența medie')
    ax.set_title('Frecvența medie a activităților în fiecare zi a săptămânii')
    ax.set_xticks(np.arange(n_weekdays) + bar_width * len(activities) / 2)
    ax.set_xticklabels(['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă','Duminică'])
    ax.legend()
    plt.show()

def plot_productivity_time_intervals():
    file = get_file_path('data_files\LifeTracking\csv\productivity_data_analysis.csv')
    df = pd.read_csv(file)
    activities_of_interest = ['uni', 'work', 'math']
    interval_columns = ['0-360', '360-720', '720-1080', '1080-1440']
    new_labels = ['00-06', '06-12', '12-18', '18-24']
    for activity in activities_of_interest:
        subset = df[df['activity'] == activity]
        subset = subset.set_index('weekday')

        subset[interval_columns].plot(kind='bar', stacked=True, figsize=(10, 6),
                    title=f'Timp mediu petrecut pe activitatea \'{activity.capitalize()} \' zilnic')

        plt.xlabel('Ziua săptămânii')
        plt.ylabel('Timp petrecut')
        plt.xticks(range(7), ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă','Duminică'],
                   rotation=45)
        plt.legend(title='Intervale de timp', labels = new_labels)
        plt.show()



def words_similarity(word1, word2):
    print(fuzz.partial_ratio(word1,word2))
    print(fuzz.ratio(word1, word2))
    print(fuzz.token_sort_ratio(word1,word2))

def extract_activity_info(activity_name, df):
    # Find the closest match in the dataset for the input activity
    activities = df.index.values
    best_match, percentage = process.extractOne(activity_name, activities)
    return best_match,percentage

#plot_analysed_data_lifeTracking()
#plot_productivity_time_intervals()