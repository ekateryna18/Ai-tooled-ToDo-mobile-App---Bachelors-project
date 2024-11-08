import os
from datetime import datetime

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.inspection import permutation_importance


def get_file_path(path):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, path)
    return file_path
def clean_word(word):
    """
    Clean characters which are not letters
    :param word: string
    :return: string
    """
    final_w = ""
    word.lower()
    for charac in word:
        if charac < 'a' or charac > 'z':
            charac = ' '
        final_w += charac
    return final_w

#------ "MsLatte" dataset processing functions ------
def process_locations(locations):
    """
    Convert locations list string to a list
    :param locations: dictionary
    :return: list
    """
    if locations['Known'] == 'yes':
        # Split the string into individual locations
        locations_list = locations['Locations'].split(',')
        # Convert individual locations to a list
        locations['Locations'] = [loc.strip() for loc in locations_list]
    locations['PublicLocations'] = clean_word(locations['PublicLocations'])
    return locations

def flatten_json_structure(data):
    """
    Aggregates column LocJudgements who can be just of 3 types (Work,Public,Home) into 3 columns
    Aggregates column TimeJudgements for each time of day and week
    :param data: dataframe from json file
    :return: dataframe with modifications
    """
    for loc in ['Loc_Home','Loc_Public','Loc_Work']:
        data[loc] = 0
        data[loc] = pd.Series(dtype='float')
    data['Time_freq'] = 0
    data['Time_freq'] = pd.Series(dtype='float')
    data['Public_locations'] = {}
    for index,row in data.iterrows():
        count = {"Loc_Home": 0, "Loc_Work": 0, "Loc_Public": 0}
        public_loc = {}
        total_loc = 0
        total_times = 0
        for judgement in row['LocJudgements']:
            for location in judgement['Locations']:
                if location.lower() == "home":
                    count["Loc_Home"] += 1
                    total_loc += 1
                elif location.lower() == "work":
                    count["Loc_Work"] += 1
                    total_loc += 1
                elif location.lower() == "public":
                    count["Loc_Public"] += 1
                    total_loc += 1
                    #if it is public it means we have the public location name
                    l = judgement["PublicLocations"]
                    val = 0
                    if l in public_loc:
                        val = public_loc.get(l)
                    public_loc[l] = val+1

        for loc, cnt in count.items():
            data.at[index, loc] = round(cnt/total_loc, 7)
        count = {"WE_morning":0,"WE_afternoon":0, "WE_evening":0,"WE_night":0,"WE_anytime":0,"WD_morning":0,"WD_afternoon":0, "WD_evening":0,"WD_night":0,"WD_anytime":0}
        for judgement in row['TimeJudgements']:
            times = judgement['Times'].split(',')
            for t in times:
                time = t.lower()
                if time == "we-morning":
                    count["WE_morning"]+=1
                    total_times+=1
                elif time == "we-afternoon":
                    count["WE_afternoon"]+=1
                    total_times+=1
                elif time == "we-afternoon":
                    count["WE_afternoon"]+=1
                    total_times+=1
                elif time == "we-night":
                    count["WE_night"]+=1
                    total_times+=1
                elif time == "we-anytime":
                    count["WE_anytime"]+=1
                    total_times+=1
                elif time == "wd-morning":
                    count["WD_morning"]+=1
                    total_times+=1
                elif time == "wd-afternoon":
                    count["WD_afternoon"]+=1
                    total_times+=1
                elif time == "wd-evening":
                    count["WD_evening"]+=1
                    total_times+=1
                elif time == "wd-night":
                    count["WD_night"]+=1
                    total_times+=1
                elif time == "wd-anytime":
                    count["WD_anytime"]+=1
                    total_times+=1
        data.at[index, 'Time_freq'] = total_times/100
        data.at[index, 'Public_locations'] = public_loc
        for daytime,cnt in count.items():
            if total_times == 0:
                print("bad")
            data.at[index, daytime] = round(cnt/total_times, 7)

    # Drop the 'LocJudgements' column
    data.drop("LocJudgements", axis=1, inplace=True)
    data.drop("TimeJudgements", axis=1, inplace=True)
    return data

def final_process_data():
    """
    Final method of processing the data
    :return:
    """
    file = get_file_path('data_files\MsLatte_dataset\MS-LaTTE.json')
    data = pd.read_json(file)
    data['LocJudgements'] = data['LocJudgements'].apply(lambda x: [process_locations(dictionary) for dictionary in x])
    data['TaskTitle'] = data['TaskTitle'].apply(lambda x: clean_word(x))
    data = data[~data['ListTitle'].str.contains('groceries', case=False, na=False)]
    data = flatten_json_structure(data)
    data.to_json('data_files\MsLatte_dataset\processed_data_mslatte.json',orient='records', lines=True)
    #data['LocJudgements'] = data['LocJudgements'].apply

#------ "Life tracking" dataset processing functions ------

def process_LifeTracking_dataset():
    """
    Normalize and process data for the algorithm's needs
    :return:
    """
    file = get_file_path('data_files\LifeTracking\csv\life_interval_data.csv')
    data = pd.read_csv(file)
    #normalize data by transforming each time format in minutes
    data['time'] = data['time'].apply(lambda x: normalize_time(x))
    data['start_time'] = data['start_time'].apply(lambda x: normalize_time(x.split(' ')[1]))
    data['weekday'] = data['date'].apply(lambda x: convert_date_to_weekday(x))
    data.to_csv('data_files\LifeTracking\csv\processed_life_data.csv', index = False)
    return data

def convert_date_to_weekday(date):
    """
    Converts a date under string format YYYY-MM-DD to the number of the day of the week
    0 for Monday
    6 for Sunday
    :param date: string
    :return: int
    """
    date_obj = datetime.strptime(date,'%Y-%m-%d').date()
    return date_obj.weekday()
def normalize_time(time):
    """
    turns time into minutes
    :param time: string
    :return: int
    """
    hours = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    return hours * 60 +minutes

def analyse_data_life_tracking():
    """
    get the average frequency of activities per each day of the week
    and productivity per parts of the day
    :return:
    """
    file = get_file_path('data_files\LifeTracking\csv\processed_life_data.csv')
    data = pd.read_csv(file)
    # calculates per each weekday how many times an activity is done
    activity_counts = data.groupby(['weekday', 'activity']).size().reset_index(name='count')
    data_unique = data.drop_duplicates(subset=["date", "activity", "weekday"])
    # calculates total of days each activity is present
    day_counts = data_unique.groupby(['weekday', 'activity'])['date'].nunique().reset_index(name='unique_days_count')
    # merges dataframes and calculates average frequency
    merged_df = pd.merge(activity_counts, day_counts, on=['weekday', 'activity'])
    merged_df['average_frequency'] = round(merged_df['count'] / merged_df['unique_days_count'])

    intervals = [0, 360, 720, 1080, 1440]
    labels = ['0-360', '360-720', '720-1080', '1080-1440']
    data['interval'] = pd.cut(data['start_time'], bins=intervals, labels=labels)
    #calculate total duration per each activity done in each weekday and time
    total_duration = data.groupby(['weekday','activity', 'interval'])['time'].sum().reset_index()
    #transform intervals into columns and assign the time duration


    data['count'] = 0
    count_duration = data.groupby(['weekday','activity', 'interval'])['count'].count().reset_index()
    total_duration = pd.merge(total_duration, count_duration, on=['weekday','activity', 'interval'])
    total_duration['time'] = total_duration['time']/total_duration['count']
    total_duration.drop("count", axis=1, inplace=True)
    total_duration = total_duration.pivot_table(values='time', index=['weekday', 'activity'], columns='interval',
                                                fill_value=0)
    # the final merged data
    merged_df = pd.merge(merged_df, total_duration, on=['weekday', 'activity'])

    #drop columns used for formula
    merged_df.drop("count", axis=1, inplace=True)
    merged_df.drop("unique_days_count", axis=1, inplace=True)
    merged_df.to_csv('data_files\LifeTracking\csv\productivity_data_analysis.csv', index = False)


#-------------Feature  importance try test
def analyze_data():
    file = get_file_path('data_files\MsLatte_dataset\processed_data_mslatte.json')
    data = pd.read_json(file, lines=True)
    #max_dict=4
    #u = data.ListTitle.unique()
    #feature_importance(data)
    f_imp(data)


def f_imp(data):
    data['PeriodOfDay'] = 0
    X = data.drop(['PeriodOfDay','TaskTitle','ListTitle','Public_locations'], axis=1)  # Replace 'PeriodOfDay' with your actual target column
    y = data['PeriodOfDay']  # Your target variable

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    feature_importances = pd.DataFrame(model.feature_importances_,
                                       index=X_train.columns,
                                       columns=['importance']).sort_values('importance', ascending=False)
    print(feature_importances)

def feature_importance(data):
    feature_names = ['Loc_Home','Loc_Public','Loc_Work', 'Time_freq','WE_morning',
               'WE_afternoon', 'WE_evening', 'WE_night', 'WE_anytime', 'WD_morning',
         'WD_afternoon', 'WD_evening', 'WD_night', 'WD_anytime']
    x = data[feature_names]
    y = data['Time_freq']
    X_train, X_val, y_train, y_val = train_test_split(x, y, random_state = 0)
    model = Ridge(alpha=1e-2).fit(X_train, y_train)
    model.score(X_val, y_val)
    r = permutation_importance(model, X_val, y_val,n_repeats = 30, random_state = 0)
    for i in r.importances_mean.argsort()[::-1]:
        if r.importances_mean[i] - 2 * r.importances_std[i] > 0:
            print(f"{feature_names[i]:<8}"f"{r.importances_mean[i]:.3f}"f" +/- {r.importances_std[i]:.3f}")

#final_process_data()
#analyze_data()
#process_LifeTracking_dataset()
#analyse_data_life_tracking()