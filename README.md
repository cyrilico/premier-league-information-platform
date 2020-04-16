# English Premier League Information Platform
Work done for a subject in Information Description, Storage and Retrieval (DAPI) in MIEIC @ FEUP, in collaboration with [@diogotorres97](https://github.com/diogotorres97).

It consists of taking a specific topic and exploring its information in different milestones. We chose **historical English Premier League games** data (between the 2014-15 and 2018-19 seasons, inclusive). Below are the different sequential milestones involved. Please check our final [**report**](https://github.com/cyrilico/english-pl-information-platform/blob/master/report.pdf) that describes all our work (including implementation details) in the format of a scientific paper.

## 1. **Data preparation and description**
We first had to obtain the data from online sources. We decided to scrape online sports platforms, namely The Guardian and SkySports, for their completeness in game information. The UML class diagram that shows all information collected and stored can be found below.

![UML Class Diagram](https://i.imgur.com/55LyTCX.png)

For each game, we collected generic information (when and where did it occur, teams involved, refereeing), as well as names of all players involved, on what team they played at the time, and different types of highlights per player. There is also a textual match report that is most useful in the next milestone. Despite most data being obtained via scraping, we still found the need to clean and refine it (e.g., for representation consistency across dates and club names).

Finally, we analyze the collected data through exploratory techniques, visualizing the distribution of different values from different fields in distinct plots.

## 2. **Search dataset through Information Retrieval (IR) techniques**
The second milestone consisted of exploring an Information Retrieval tool and its main features, while also answering some identified retrieval tasks given the context of our data (see section 2.4 of our report). We opted to use **Solr** as our IR tool.

We were able to explore the tool's capabilities both during indexing and search processes. For the former, we defined custom fields tailored to our data with custom analyzers (a sequence of a tokenizer and further filters). For the latter, we explored different relevance adjustment techniques, such as *field boosting*, *phrase queries*, *negative matches*, *query-independent boosts* and *wildcard queries*. To evaluate the results given by our system, we used both *Precision at 10 (P@10)* and *Average Precision (AP)*.

## 3. **Construct and Query Knowledge Graph (Ontology)**
The final milestone's goal was to represent and search data from a new perspective by using Semantic Web tools and technologies. The first step was to identify existing ontologies that would help contextualize our information without the need to "reinvent the wheel". For this, we reused concepts from the **DBPedia Ontology**. This also facilitates further integration of the developed ontology into new ones. The figures below present the classes, data properties and object properties defined, respectively. Note the usage of the prefixes *dbo* and *dbp* (DBPedia Object and DBPedia Property) signaling the reusage of existing concepts. For details on each resource (e.g., domain or functionality properties), refer to the report.

| Classes | Data properties | Object properties
| --- | --- | --- |
| ![Ontology Classes](https://imgur.com/daum8PT.png) | ![Ontology data properties](https://i.imgur.com/pPynZ43.png) | ![Ontology object properties](https://i.imgur.com/bW3uE1z.png) |

Finally, we answered the remaining retrieval tasks identified (that weren't already covered in the IR section) by using **SPARQL**.
