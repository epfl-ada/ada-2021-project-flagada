import bz2
import json
import re
from datetime import date, datetime

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from tqdm.notebook import tqdm

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
analyzer = SentimentIntensityAnalyzer()

weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


################################################## LINK QIDS ##########################################################

def qid_to_label(QID, labels):
    """ Return the label corresponding to the QID. Labels should be a dataframe loaded as :
    labels = pd.read_csv('wikidata_labels_descriptions_quotebank.csv.bz2', compression='bz2', index_col='QID')
    """
    try:
        label = labels.loc[QID]['Label']
    except:
        raise ValueError('The QID \'' + QID + '\' does not appear in the repertoire labels') from None

    return label


def speaker_to_attributes(QID, attributes):
    """ Return the (interesting for us) attributes corresponding to the QID of a speaker. Attributes should
     be a dataframe loaded as :
    attributes = pd.read_parquet('speaker_attributes.parquet')
    """
    line = attributes[attributes.id == QID]
    if (len(line) == 0):
        raise ValueError('The QID \'' + QID + '\' does not appear in the repertoire attributes') from None
    
    return line[['date_of_birth', 'nationality', 'gender', 'ethnic_group', 'occupation', 'party', 'religion']].to_dict(
        orient='records')[0]


def speaker_to_labels(QID, attributes, labels):
    """ Return the (interesting for us) attributes corresponding to the QID of a speaker, 
    readable by a human (not with QIDS). Attributes and labels should be dataframes loaded as :
    attributes = pd.read_parquet('speaker_attributes.parquet')
    labels = pd.read_csv('wikidata_labels_descriptions_quotebank.csv.bz2', compression='bz2', index_col='QID')
    """
    dic = speaker_to_attributes(QID, attributes)
    keys = ['nationality', 'gender', 'ethnic_group', 'occupation', 'party', 'religion']
    if (dic['date_of_birth'] is not None):
        dic['date_of_birth'] = dic['date_of_birth'][0]  # Reduce from list of 1 string to string
    else:
        dic['date_of_birth'] = 'None'
    for key in keys:
        if (dic[key] is not None):
            if (len(dic[key]) == 1):
                dic[key] = qid_to_label(dic[key][0], labels) # Reduce from list of 1 object to object
            else:
                new_value = []
                for q in dic[key]:
                    new_value.append(qid_to_label(q, labels))
                dic[key] = new_value
        else:
            dic[key] = 'None'
            
    return dic


################################################# UTILITIES ##########################################################

def find_word(quote, lexic):
    """ Finds if any of the words in lexic are present in string quote 
        This looks for both uppercase and lower case character, and characters such as .,(! etc...
        Example : find_word('Charles is so HOT.', ['hot', 'temperature']) --> True
                  find_word('The coalition', ['coal']) --> False (it does not count as true appearance in another word)
        """
    for word in lexic:
        if(re.search(rf'\b{word}\b', quote, flags=re.IGNORECASE)):
            return True
    return False


# From previous idea
def retrieve_day(Date):
    """ Retrieve the day from a date with format 'YYYY-MM-DD hh:mm:ss' where Y is years, M months, D day, h hours,
        m minut and s seconds 
        Needs the following import :
        from datetime import datetime
        """

    try:                        
        _date = datetime.strptime(Date, '%Y-%m-%d %H:%M:%S') # Convert to a datetime object and check that the format is correct and the numbers are valid
    except ValueError:
        raise ValueError('The string \'' + Date + '\' does not match the format \'YYYY-MM-DD hh:mm:ss\'') from None # Customize the error message

    if (_date.year not in [2015, 2016, 2017, 2018, 2019, 2020]): # Check that the year is in the correct interval and that we do not have wrong data
        raise ValueError(f'The year {_date.year} that you provided is not between 2015 and 2020 (inclusive).')

    weekday = datetime.weekday(_date) # Obtain the weekday from 1 (monday) to 7 (sunday)

    return weekdays[weekday]


def weekdays_stats(df):
    """ Print simple statistics about the sentiment as a function of weekdays.
        The input df needs to contain the day column.
    """
    for d in weekdays:
        print(d, ':')
        positives = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a > 0])
        negatives = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a < 0])
        total = len([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        all_mean = np.mean([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound'))])
        no_zero_mean = np.mean([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        print("Proportion of positives: ", positives/total)
        print("Proportion of negatives: ", negatives/total) 
        print("Mean of the compounds :", all_mean)
        print("Mean of the compounds without the neutral results :", no_zero_mean)



def create_frame(filename, N):
    """ Creates a DataFrame with the N first rows of the file with filename (being a json.bz2 file)
        It is useful to load small portions and test things. 
    """
    list_of_dicts = []
    with bz2.open(filename, 'rb') as s_file:
        for i, instance in enumerate(s_file):
            if (i>N-1):
                break
            instance = json.loads(instance) # loading a sample
            list_of_dicts.append(instance)
        
    return pd.DataFrame(list_of_dicts)



def frequence_words(sentence):
    """ Finds the frequency of appearance of all (important) words in the sentence
    """
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.append('climate')
    stop_words.append('change')
    stop_words.append('warming')
    stop_words.append('global')
    tokenizer = nltk.RegexpTokenizer(r"\w+") # To remove punctuation
    tokens = tokenizer.tokenize(sentence)
    tokens = [word.lower() for word in tokens] # Put everything to lowercase
    filtered_sentence = [word for word in tokens if (word not in stop_words)]  # Remove stop words
    filtered_sentence = [word for word in filtered_sentence if (not word.isdecimal())] # Remove full numeric words (e.g '2015')

    words, count = np.unique(filtered_sentence, return_counts=True)
    frequency = {}
    for i, word in enumerate(words):
        frequency[word] = count[i]

    return frequency

def capital_letter_keywords(quotes_2020, date_choice) :
    """ Finds most frequent keywords for a given date, starting with a capital letter
    """
    quotation_test= quotes_2020[quotes_2020['date'].astype(str)== date_choice].quotation
    flat_list = [sublist[i] for sublist in quotation_test.str.split() for i in range(len(sublist)) ]
    total_quotation = " ".join(flat_list)
    
    stop_words = set(stopwords.words('english'))
    stop_words.add('climate')
    stop_words.add('Climate')
    stop_words.add('change')
    stop_words.add('warming')
    stop_words.add('environmental')
    stop_words.add('threat')
    stop_words.add('emergency ')
    stop_words.add('global')
    stop_words.add('world')
    word_tokens = word_tokenize(total_quotation)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence_join = " ".join(filtered_sentence)
    filtered_sentence_df = pd.Series(filtered_sentence)
    filtered_sentence_df = filtered_sentence_df[filtered_sentence_df.apply(lambda x : len(x)>3)]
    count_capital_letter = pd.Series([ x for x in filtered_sentence if  x[0].isupper()]).value_counts()
    count_capital_letter = count_capital_letter[count_capital_letter>(0.03*len(quotation_test))]
    
    return filtered_sentence_df, count_capital_letter


def all_keywords(quotes_2020, date_choice) :
    """ Finds most frequent keywords for a given date
    """
    quotation_test= quotes_2020[quotes_2020['date'].astype(str)== date_choice].quotation
    flat_list = [sublist[i] for sublist in quotation_test.str.split() for i in range(len(sublist)) ]
    
    total_quotation = " ".join(flat_list)
    
    stop_words = set(stopwords.words('english'))
    stop_words.add('climate')
    stop_words.add('Climate')
    stop_words.add('change')
    stop_words.add('warming')
    stop_words.add('environmental')
    stop_words.add('threat')
    stop_words.add('emergency ')
    stop_words.add('global')
    stop_words.add('world') 
    word_tokens = word_tokenize(total_quotation)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence_join = " ".join(filtered_sentence)
    filtered_sentence_df = pd.Series(filtered_sentence)
    filtered_sentence_df = filtered_sentence_df[filtered_sentence_df.apply(lambda x : len(x)>3)]
    count_words =filtered_sentence_df.value_counts()
    count_words = count_words[count_words>(0.05*len(quotation_test))]
    
    return filtered_sentence_df, count_words


def frequence_words_frame(frame, Date):
    """ Finds the frequency of all the words present in the dataframe for a certain date.
    
        Date must be a date object (e.g Date = date.fromisoformat('2015-04-12'))
    """
    quotes = frame[frame['date'].dt.date == Date].quotation.to_list()
    total = ' '.join(quotes)

    return frequence_words(total)


############################################# TO CREATE DATASETS ######################################################

def save_df_with_day(filein, fileout):
    """ Save a the dataset with the day column added
    """
    with bz2.open(filein, 'rb') as s_file:
        with bz2.open(fileout, 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                day = retrieve_day(instance['date'])
                instance['day'] = day
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file


def save_lexic(filein, fileout, lexic):
    """ Save the lexic (climate) related quotes of filein into fileout
        lexic is a list of words
        example : lexic = ['climate change', 'climate emergency', 'global warming', 'COP21', 'COP26']
    """
    with bz2.open(filein, 'rb') as s_file:
        with bz2.open(fileout, 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                if(find_word(instance['quotation'], lexic)):
                    d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file



def save_lexic_with_attributes(filein, fileout, lexic, attributes, labels):
    """ Save the lexic (climate) related quotes of filein into fileout, linking qids of known speaker to their 
        attributes (if the speaker has only 1 qid, otherwise we cannot know which one to take)
        ATTENTION : it is inefficient (but works) since for each quote related to climate, the code will need to scan 
                    in the entire attributes frame (which is large) for a matching QID

        lexic is a list of words (e.g lexic = ['climate change', 'climate emergency'])
        atrributes and labels are dataframe loaded as :
        attributes = pd.read_parquet('speaker_attributes.parquet')
        labels = pd.read_csv('wikidata_labels_descriptions_quotebank.csv.bz2', compression='bz2', index_col='QID')
    """

    keys = ['date_of_birth', 'nationality', 'gender', 'ethnic_group', 'occupation', 'party', 'religion']

    with bz2.open(filein, 'rb') as s_file:
        with bz2.open(fileout, 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                if(find_word(instance['quotation'], lexic)):
                    if (len(instance['qids']) == 1):
                        try:
                            dic = speaker_to_labels(instance['qids'][0], attributes, labels)
                            for key in dic.keys():
                                instance[key] = dic[key]
                        except:
                            pass
                    else:
                        for key in keys:
                            instance[key] = 'None'
                    d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file


def save_all_years(directory):
    """ Save the quotes from all years in one single file from the files of each years"""

    fileout = directory + 'quotes-all-years.json.bz2'
    years = [2015, 2016, 2017, 2018, 2019, 2020]
    with bz2.open(fileout, 'wb') as d_file:
        for year in tqdm(years):
            filein = directory + f'quotes-{year}.json.bz2' 
            with bz2.open(filein, 'rb') as s_file:
                for instance in s_file:
                    instance = json.loads(instance) # loading a sample
                    d_file.write((json.dumps(instance)+'\n').encode('utf-8'))



def save_df_with_sentiment(filename):
    """ Save a dataset with a column containing the results of the sentiment analysis performed on the quotation
    """
    with bz2.open(filename, 'rb') as s_file:
        with bz2.open(f'sentiment_{filename}', 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                sentiment = analyzer.polarity_scores(instance['quotation'])
                instance['sentiment'] = sentiment
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file


################################################# PLOTS ###############################################################


def weekdays_sent_plot(df):
    """ Plots the histogram of the sentiment as a function of weekdays
    """
    for d in weekdays:
        sns.histplot([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        plt.title(d)
        plt.xlabel('Sentimental score')
        plt.ylabel('Number of quotes')
        plt.show()


# Plots
def plot_sentiment(df):
    """ Plots the compound value of the sentiment
    """
    sns.histplot(df['sentiment'].apply(lambda x: x.get('compound')))
    plt.show()