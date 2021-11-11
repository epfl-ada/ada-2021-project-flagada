import pandas as pd
from datetime import datetime
import bz2
import json
from tqdm.notebook import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# From previous idea
def retrieve_day(Date):
    """ Retrieve the day from a date with format 'YYYY-MM-DD hh:mm:ss' where Y is years, M months, D day, h hours,
        m minut and s seconds 
        Needs the following import :
        from datetime import datetime
        """

    try:                        
        date = datetime.strptime(Date, '%Y-%m-%d %H:%M:%S') # Convert to a datetime object and check that the format is correct and the numbers are valid
    except ValueError:
        raise ValueError('The string \'' + Date + '\' does not match the format \'YYYY-MM-DD hh:mm:ss\'') from None # Customize the error message

    if (date.year not in [2015, 2016, 2017, 2018, 2019, 2020]): # Check that the year is in the correct interval and that we do not have wrong data
        raise ValueError(f'The year {date.year} that you provided is not between 2015 and 2020 (inclusive).')

    weekday = datetime.isoweekday(date) # Obtain the weekday from 1 (monday) to 7 (sunday)

    # There are no switch/case statement in Python <= 3.10...
    if (weekday == 1):
        return 'Monday'
    elif (weekday == 2):
        return 'Tuesday'
    elif (weekday == 3):
        return 'Wednesday'
    elif (weekday == 4):
        return 'Thursday'
    elif (weekday == 5):
        return 'Friday'
    elif (weekday == 6):
        return 'Saturday'
    else:
        return 'Sunday'

def save_df_with_day(filename):
    with bz2.open(filename, 'rb') as s_file:
        with bz2.open(f'day_{filename}', 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                day = retrieve_day(instance['date'])
                instance['day'] = day
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file

def weekdays_stats(df):
    for d in weekdays:
        print(d, ':')
        positives = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a > 0])
        negatives = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a < 0])
        total = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        all_mean = np.mean([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound'))])
        no_zero_mean = np.mean([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        print("Proportion of positives: ", positives/total)
        print("Proportion of negatives: ", negatives/total) 
        print(all_mean)
        print(no_zero_mean)

def weekdays_sent_plot(df):
    for d in weekdays:
        print(d, ':')
        sns.histplot([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        plt.show()

# Utils
def create_frame(filename, N):
    """ Creates a DataFrame with the N first rows of the file with filename 
        It is useful to load small portions and test things.            """
    list_of_dicts = []
    with bz2.open(filename, 'rb') as s_file:
        for i, instance in enumerate(s_file):
            if (i>N-1):
                break
            instance = json.loads(instance) # loading a sample
            list_of_dicts.append(instance)
        
    return pd.DataFrame(list_of_dicts)

def save_df_with_sentiment(filename):
    with bz2.open(filename, 'rb') as s_file:
        with bz2.open(f'sentiment_{filename}', 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                sentiment = analyzer.polarity_scores(instance['quotation'])
                instance['sentiment'] = sentiment
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file

def filter_df_by_keywords(df, searchfor):
    return df.loc[df['speaker'] != 'None'][df['quotation'].str.contains('|'.join(searchfor))]


# Plots
def plot_sentiment(df):
    sns.histplot(df['sentiment'].apply(lambda x: x.get('compound')))
    plt.show()