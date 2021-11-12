# Which events have pushed the climate debate forward in recent history ?

## Abstract 


Climate change became a real threat in the last decades. Populations started to be aware of it and the climate debate diffused around the world. With the Quotebank dataset, it is possible to map the relation between the impacts of climate change and public opinion. Major events seem to inflate this debate. Indeed, human nature leads us to be concerned either by events impacting our personal lives, or by spectacular ones. As such, we seek to study the reaction of media with respect to events and try to identify their nature. In that way, we can better understand the human psychology regarding the climate threat and how the reactions evolved along the years. To do so, we look for the highest number of occurences of climate change mentions and use the evoked keywords to determine if it corresponds to a particular event.

## Research questions

* Can the number of quotes about climate change be linked to particular events ?
* Can we identify the nature of the event according to the content of the quotes on a given day?
* What kind of event is the most impactful ? (natural event, political summit, social gathering...)
* How different political parties handle these events (using sentiment analysis)

## Methods

We first start with a sanity check to remove all data rows with an unreadable date. Then we add a column to the data set containing the day of the week. 

The next task we need to tackle is to extract quotes that are related to climate change. For this we established a list of words related to this subject and filtered out the quotes that didn't contain any of those words. This method seems sufficient during our testing and was much more efficient than using a pre-trained classifier.

We will also expand the dataset to add information about the speakers (using Wikidata), for instance, their political party, if they are politicians (for this part we might have to reduce our scope to only the US, as it will simplify the identification of political views). During our testing we also performed sentiment analysis, using a pre-trained model shipped with `nltk`, this might become useful to answer questions about how different people adress the climate issue.

Once we have constructed this dataset, we will want to visualize the frequency of quotes regarding the subject and see if any peaks are detectable. To detect the peaks we will implement a method to find local maxima on different scales (weeks or days). One of the main goals of this project is to create a baseline trend for the increase of climate discussions and to identify the outliers to try and link them to particular events in recent history. To be able to detect which event corresponds to a particular set of quotes, we also study the most common words cited using `nltk`, by first removing stopwords, punctuation and also words we used to identify quotes related to climate change.

## Proposed timeline

![timeline](https://user-images.githubusercontent.com/9378265/141483454-d3a8cd20-4bd4-468f-b0b8-592ef4c423a6.png)

* (N.B: the word count of this timeline is approximately 250 words.) *

## Organization within the team

| |  Cyril | Nicolas  | Adrien  | Charles  |
|---|---|---|---|---|
| Week 9  | 1 | 1 | 1 | 1 |
| Week 10  | 2 | 3 | 3 | 3 |
|  Week 11 | 5 | 4 | 5 | 4 |
|  Week 12 | 7 | 6 | 6 | 7 |
| Week 13  |7/8| 8 | 8 |7/8|

## Structure of the files

* #### `functions.py`

In this Python file, we aggregated most of our functions in order to visually clarify our notebook files.

* #### `requirements.txt`

This files summaries all of the necessary libraries with their respective versions.

* #### `weekdays.ipynb`

First, we had an initial idea to study the sentiment of the quotes according to the days of the week. However, after some analyses on the data, in `weekdays.ipynb`, we quickly realised it was not the most interesting subject. However, these preliminary manipulations on the dataset allowed us to better understand its structure and size. We thus decided to keep it and explain our reasoning. In this context, we expanded the original dataset with a column stating the day related to the date of the row. We kept using these new data files for the rest even though it is not useful for climate change analysis.

* #### `playground.ipynb`

This notebook purpose is to sort the data according to our final topic : the impact of climate change events on the press releases. Indeed, we only kept quotes related to the environment using keywords and we made primary experiments with the data.

* #### `proof_of_concept.ipynb`

This file is the heart of this milestone. It gives the main statistical manipulations on the data and provides an initial study on the 2020 dataset. Within it, we manage to identify the nature of a climate related event in january just by looking at the frequency of keywords in the quotes (fire, wildfire, Australia,...).
