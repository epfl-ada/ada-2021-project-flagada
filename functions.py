import pandas as pd
from datetime import datetime
from datetime import date
import bz2
import json
import re
from tqdm.notebook import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
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
    for key in keys:
        if (dic[key] is not None):
            if (len(dic[key]) == 1):
                dic[key] = qid_to_label(dic[key][0], labels) # Reduce from list of 1 object to object
            else:
                new_value = []
                for q in dic[key]:
                    new_value.append(qid_to_label(q, labels))
                dic[key] = new_value
            
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

    weekday = datetime.isoweekday(_date) # Obtain the weekday from 1 (monday) to 7 (sunday)

    #
    for i in range(7) :
        if (weekday == i+1) :
            return weekdays[i]
        


def filter_df_by_keywords(df, searchfor):
    return df.loc[df['speaker'] != 'None'][df['quotation'].str.contains('|'.join(searchfor))]



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
    filtered_sentence = [word for word in filtered_sentence if (word.isdecimal())] # Remove full numeric words (e.g '2015')

    words, count = np.unique(filtered_sentence, return_counts=True)
    frequency = {}
    for i, word in enumerate(words):
        frequency[word] = count[i]

    return frequency



def frequence_words_frame(frame, Date):
    """ Finds the frequency of all the words present in the dataframe for a certain date.
    
        Date must be a date object (e.g Date = date.fromisoformat('2015-04-12'))
    """
    quotes = frame[frame['date'].dt.date == Date].quotation.to_list()
    total = ' '.join(quotes)

    return frequence_words(total)


############################################# TO CREATE DATASETS ######################################################

def save_df_with_day(filein, fileout):
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
                            instance[key] = None
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file




def save_df_with_sentiment(filename):
    with bz2.open(filename, 'rb') as s_file:
        with bz2.open(f'sentiment_{filename}', 'wb') as d_file:
            for instance in tqdm(s_file):
                instance = json.loads(instance) # loading a sample
                sentiment = analyzer.polarity_scores(instance['quotation'])
                instance['sentiment'] = sentiment
                d_file.write((json.dumps(instance)+'\n').encode('utf-8')) # writing in the new file


################################################# PLOTS ###############################################################


def weekdays_sent_plot(df):
    for d in weekdays:
        sns.histplot([a for a in df.loc[df['day'] == d]['sentiment'].apply(lambda x: x.get('compound')) if a != 0])
        plt.title(d)
        plt.xlabel('Sentimental score')
        plt.ylabel('Number of quotes')
        plt.show()


# Plots
def plot_sentiment(df):
    sns.histplot(df['sentiment'].apply(lambda x: x.get('compound')))
    plt.show()