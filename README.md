# Is the climate debate unequal ?

## Abstract 

It is no surprise to anyone reading this that climate change has been a topic of polarizing discussion for the last few years. Indeed, it becomes more and more apparent in the signs from nature (floods, heatwaves and so on) that something is happening and our societies are reacting. Consequently, measures are taken by decision makers about how to mitigate it. Scientists are getting interviewed, politicians give speeches and all of this is delivered by the media. Such influence can be studied through the analysis of who and what they quote in their articles. The Quotebank dataset offers such a possibility, thanks to its 178M quotes from which climate change related quotes can be filtered. In this sense, the goal of this study is to better understand how the climate change debate has been evolving with a focus on a few events that were pillars in the discussion.

## Research questions

* Can the number of quotes about climate change be linked to particular events only by using keywords?
* Can we identify the nature of the event according to the content of the quotes on a given day?
* What kind of event is the most impactful ?
* Optional : How different political parties handle these events (using sentiment analysis)

## Methods

The first task we need to tackle is to extract quotes that are related to climate change. For this we established a list of words related to this subject and filtered out the quotes that did not contain any of those words. This method seems sufficient during our testing and was much more efficient than using a pre-trained classifier.

We will also expand the dataset to add information about the speakers (using Wikidata), for instance, their political party, if they are politicians (maybe focused on the USA for parties consistency). During our testing we also performed sentiment analysis, using a pre-trained model shipped with `nltk`, this might become useful to answer questions about how different people adress the climate issue.

Once we have constructed this dataset, we will want to visualize the frequency of quotes regarding the subject and see if any peaks are detectable. To detect the peaks we will implement a method to find local maxima on different scales (weeks or days). One of the main goals of this project is to create a baseline trend for the increase of climate discussions and to identify the outliers to try and link them to particular events. To be able to detect which event corresponds to a particular set of quotes, we also study the most common words cited using `nltk`, by first removing stopwords, punctuation and also words we used to identify quotes related to climate. 

We could try in the future in our datastory blog to incorporate interactiveness to the data. This would be done by allowing the viewer to "click" on peakdays, discover by themselves the most mentioned words and deduce what would be the event.

## Timeline

![timeline](https://user-images.githubusercontent.com/9378265/141483454-d3a8cd20-4bd4-468f-b0b8-592ef4c423a6.png)

_(N.B: the wordcount of this timeline is approximately 250 words.)_

## Team Organization

| |  Cyril | Nicolas  | Adrien  | Charles  |
|---|---|---|---|---|
| Week 9  | 1 | 1 | 1 | 1 |
| Week 10  | 2 | 3 | 3 | 3 |
|  Week 11 | 5 | 4 | 5 | 4 |
|  Week 12 | 7 | 6 | 6 | 7 |
| Week 13  |7/8| 8 | 8 |7/8|

## Structure of files

* #### `functions.py`

In this Python file, we aggregated most of our functions in order to clarify our notebook files.

* #### `requirements.txt`

This files summaries all of the necessary libraries with their respective versions.

* #### `plots.ipynb`

A notebook that contains all the functions needed to obtain the different plots

* ### `map_and_occupation.ipynb`

As its name suggests, this notebook is used to obtain the map plot and also the occupation of the people quoted.
