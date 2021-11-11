# Which events have pushed the climate change debate forward in recent history ?

## Abstract 


Climate change has became a real threat in the last decades. At the same time, populations start to be aware of it and the climate debate is diffusing around the world. Here, with the Quotebank data set, it is possible to map the relation between the impacts of climate change and the public opinion. The last reports of the IPCC and the COP conferences might highlight a really step towards the environmental transition from the world leaders. This project aims to study how much the climate debate has inflated along the years. Using the Quotebank dataset, we can analyse how much climate change is dealt in the press, according to different factors. Comparing these factors can help understand what are the reasons people talk about these issues. Is it catastropheses, Greta Thunberg's speeches, political parties statements, street demonstrations...? Many reasons lead to these debates and this project can help people caring about the environment to understand how and when it takes over the public discussion.

## Research questions

Our first question would be to study the impact of climate related events on the number of quotes about climate change. How much does a speech of Donald Trump on fossil fuels stimulate the number of quotes related to the environment? This would be an example of questions that can be answered by such an analysis. We can then classify these types of events and study which ones have the biggest impacts on the public press. We will also organize the quotes with lexical field to see 

* Can the number of quotes about climate change be linked to particular events ?
* Can these events be identified using the nationnality of the speakers and the most common words cited ?
* What kind of event is the most impactful ? (natural event, political summit, social gathering...)
* How different political parties handle these events (using sentiment analysis)

## Methods

We first start with a sanity check to remove all data rows with an unreadable date. Then we add a column to the data set containing the day of the week. 

The next task we need to tackle is to extract quotes that are related to climate change. For this we established a list of words related to this subject and filtered out the quotes that didn't contain any of those words. This method seems sufficient during our testing and was much more efficient than using a pre-trained classifier.

We will also expand the dataset to add information about the speakers (using Wikidata), for instance, their political party, if they are politicians (for this part we might have to reduce our scope to only the US, as it will simplify the identification of political views). During our testing we also performed sentiment analysis, using a pre-trained model shipped with `nltk`, this might become useful to answer questions about how different people adress the climate issue.

Once we have constructed this dataset and added the classification labels to it, we will want to visualize the frequency of quotes regarding the subject and see if any peaks are detectable. One of the main goals of this project is to create a baseline trend for the increase of climate discussions and to identify the outliers to try and link them to particular events in recent history.

## Proposed timeline



## Organization within the team

| |  Cyril | Nicolas  | Adrien  | Charles  |
|---|---|---|---|---|
| Week 9  |   |   |   |   |
| Week 10  |   |   |   |   |
|  Week 11 |   |   |   |   |
|  Week 12 |   |   |   |   |
| Week 13  |   |   |   |   |
