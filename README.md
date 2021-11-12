# Which events have pushed the climate debate forward in recent history ?

## Abstract 


Climate change has became a real threat in the last decades. At the same time, populations start to be aware of it and the climate debate is diffusing around the world. Here, with the Quotebank data set, it is possible to map the relation between the impacts of climate change and the public opinion. The last reports of the IPCC and the COP conferences might highlight a really step towards the environmental transition from the world leaders. This project aims to study how much the climate debate has inflated along the years. Using the Quotebank dataset, we can analyse how much climate change is dealt in the press, according to different factors. Comparing these factors can help understand what are the reasons people talk about these issues. Is it catastropheses, Greta Thunberg's speeches, political parties statements, street demonstrations...? Many reasons lead to these debates and this project can help people caring about the environment to understand how and when it takes over the public discussion.

## Research questions

* Can the number of quotes about climate change be linked to particular events ?
* Can we identify the nature of the event according to the content of the quotes on a given day?
* What kind of event is the most impactful ? (natural event, political summit, social gathering...)
* How different political parties handle these events (using sentiment analysis)

## Methods

We first start with a sanity check to remove all data rows with an unreadable date. Then we add a column to the data set containing the day of the week. 

The next task we need to tackle is to extract quotes that are related to climate change. For this we established a list of words related to this subject and filtered out the quotes that didn't contain any of those words. This method seems sufficient during our testing and was much more efficient than using a pre-trained classifier.

We will also expand the dataset to add information about the speakers (using Wikidata), for instance, their political party, if they are politicians (for this part we might have to reduce our scope to only the US, as it will simplify the identification of political views). During our testing we also performed sentiment analysis, using a pre-trained model shipped with `nltk`, this might become useful to answer questions about how different people adress the climate issue.

Once we have constructed this dataset, we will want to visualize the frequency of quotes regarding the subject and see if any peaks are detectable. One of the main goals of this project is to create a baseline trend for the increase of climate discussions and to identify the outliers to try and link them to particular events in recent history. To be able to detect which event corresponds to a particular set of quotes, we also study the most common words cited using `nltk`, by first removing stopwords, punctuation and also words we used to identify quotes related to climate change.

## Proposed timeline

![timeline](https://user-images.githubusercontent.com/9378265/141483454-d3a8cd20-4bd4-468f-b0b8-592ef4c423a6.png)


## Organization within the team

| |  Cyril | Nicolas  | Adrien  | Charles  |
|---|---|---|---|---|
| Week 9  | 1 | 1 | 1 | 1 |
| Week 10  | 2 | 3 | 3 | 3 |
|  Week 11 | 5 | 4 | 5 | 4 |
|  Week 12 | 7 | 6 | 6 | 7 |
| Week 13  |7/8| 8 | 8 |7/8|
