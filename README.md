
# Portfolio2Keyword

*Portfolio2Keyword* (p2k) is an algorithm written in python for automatic keyword extraction from a collection of documents and was developed for the project in the text mining course (732A92) at Linköping University. The goal of the algorithm is to provide users with a simple and interactive tool with the intention to aid the user in the process of information retrieval. The algorithm is by no means a complete toolset but can nonetheless introduce time-savings and valuable insights to the user.  

P2k also introduce an eﬃcient ranking algorithm that, despite its simplicity, extracts semantic coherent keywords to be used as building blocks for future queries. The proposed algorithm, HarmonicRank, is compared to the widely used PageRank algorithm
  
For a detailed description of the algorithm, read the project [report]() 


## Requirements

The following python modules have been used in the implementation of the algorithm

```
nltk 3.2.2
networkx 2.0
spacy 2.0.5
scipy.stats 1.0.0
operator


```

You may also need to download certain module dependent assets

```bash

python -m spacy download en
python -m nltk.downloader stopwords

```

____


## Portfolio2Keyword Usage

### Arguments

The p2k algorithm takes three arguments:

```
portfolio:
            The corpus represented as a python list
stopwords:
            A python set of stopwords (optional). If not provided, the function 
            algorithm will use the standard set of stopwords from the nltk module.
tags:
            A python set of Part-of-Speech (POS) tags. Default is None, used if 
            the user only wants to include keywords of a certain word-type`
```
    
    
## Example

In the following example, the algorithm will be run in two setups for demonstrating the use of POS-tags.

* Setup 1: All POS-tags
* Setup 2: Subset of POS-tags, namely adjectives, nouns and verbs


```python
import nltk
import portfolio2keyword as p2k
import networkx as nx

stopwords = set(nltk.corpus.stopwords.words('english'))
pos_tags = set(['NOUN', 'VERB', 'ADJ'])
```

Alternatively, the user can choose to extend the set of stopwords by adding domain-specif stopwords using the _union_ method.


```python
stopwords = stopwords.union(set('hello'))
```

The portfolio can consist of text strings of any sort, ranging from simple sentences to full-text documents. 

In this example, we will use the following texts:

> “Text mining, also referred to as text data mining, roughly equivalent to text analytics, is the process of deriving high-quality information from text.”


---

### Initialization 


```python
portfolio = ["Text mining, also referred to as text data mining, roughly equivalent to text analytics, is the process of deriving high-quality information from text"]

# Setup 1
portfolio_posAll = p2k.portfolio2keyword(portfolio, stopwords= stopwords)

# Setup 2
portfolio_posSubset = p2k.portfolio2keyword(portfolio, stopwords= stopwords, tags=pos_tags)
```

__Summary:__  

The user can also extract some useful summary to get some useful insights using the *get_summary()* method. 

In this example, we can see that by using a subset of POS-tags we avoid generating two additional candidate keywords.


```python
portfolio_posAll.get_summary()
```

    Number of Keyword Candidates 13
    Number of Documents 1



```python
portfolio_posSubset.get_summary()
```

    Number of Keyword Candidates 11
    Number of Documents 1


### Ranking and Keywords Extraction

The extraction of relevant keywords can be done using a ranking algorithm of choice. 

The two ranking algorithms included in p2k are, as of this moments, the PageRank and the HarmonicRank algorithm.


```python
# Setup 1
keywords_posAll_PR = portfolio_posAll.extract_keywords_pagerank()
keywords_posAll_HR = portfolio_posAll.extract_keywords_harmonic()

# Setup 2
keywords_posSubset_PR = portfolio_posSubset.extract_keywords_pagerank()
keywords_posSubset_HR = portfolio_posSubset.extract_keywords_harmonic()
```

__All POS-tags (Setup 1):__
 


```python
print("{0:15}  {1:15}".format("PageRank","HarmonicRank"))
print("-"*30)
for i in range(10):
    print("{0:15} | {1:15}".format(keywords_posAll_PR[i][0],keywords_posAll_HR[i][0]))
```

    PageRank         HarmonicRank   
    ------------------------------
    text            | text           
    high            | datum          
    quality         | high           
    also            | mining         
    roughly         | quality        
    equivalent      | also           
    refer           | roughly        
    datum           | analytic       
    mining          | equivalent     
    information     | derive         


__Subset of POS-tags (Setup 2):__


```python
print("{0:15}  {1:15}".format("PageRank","HarmonicRank"))
print("-"*30)
for i in range(8):
    print("{0:15} | {1:15}".format(keywords_posSubset_PR[i][0],keywords_posSubset_HR[i][0]))
```

    PageRank         HarmonicRank   
    ------------------------------
    text            | text           
    high            | high           
    quality         | datum          
    mining          | mining         
    datum           | quality        
    information     | derive         
    derive          | analytic       
    analytic        | information    


### Algorithm Interaction

The P2K algorithm also allows users for interaction through the following methods

* getNeighbor()
* remove_nodes()

__Creating multi-word keyword:__

In cases when the user wants to create multi-word keywords, the user can do so by using the _getNeighbor()_ method and thereby extracting candidate keywords that co-occur with the word of interest. As seen in the example below, the keyword 'text' co-occur with the words such as mining and datum (singular form of _data_).


```python
portfolio_posAll.getNeighbor("text")
```




    ['mining', 'analytic', 'datum']



__Removing undesired keywords:__

The user can also choose to remove undesired keywords and thereafter rerun the ranking algorithm


```python
portfolio_posAll.remove_nodes("high")

keywords_posAll_PR_update = portfolio_posAll.extract_keywords_pagerank()
keywords_posAll_HR_update = portfolio_posAll.extract_keywords_harmonic()

print("{0:15}  {1:15}".format("PageRank","HarmonicRank"))
print("-"*30)
for i in range(10):
    print("{0:15} | {1:15}".format(keywords_posAll_PR_update[i][0],keywords_posAll_HR_update[i][0]))

```

    PageRank         HarmonicRank   
    ------------------------------
    text            | text           
    also            | mining         
    roughly         | datum          
    information     | quality        
    equivalent      | refer          
    refer           | also           
    quality         | roughly        
    datum           | analytic       
    mining          | equivalent     
    analytic        | information    

