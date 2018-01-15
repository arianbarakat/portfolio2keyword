from __future__ import unicode_literals
import nltk
import itertools
import spacy
from operator import itemgetter
from math import log
import networkx as nx
from scipy.stats import hmean

class portfolio2keyword():

        def _doc_normalization(self, raw_doc):
            items = [".", ",", "!", "-", "?", "\/", "=", "<",">", ")", "("]
            doc = raw_doc
            for item in items:
                doc = doc.replace(item, " ")

            return(doc)

        def _candidate_token_filter(self, token):
            """
            Function to filter spacy processed token.
            Used pref. in a list comprehensions
            """

            if not self.tags == None:
                try:
                    if not token.is_punct and token.pos_ in self.tags and not token in self.stopwords and len(token) > 1:
                        return(token.lemma_)
                except:
                    pass

            else:
                try:
                    if not token.is_punct and not token in self.stopwords and len(token) > 1:
                        return(token.lemma_)
                except:
                    pass

        def _doc_token_filter(self, token):
            """
            Function to filter spacy processed token.
            Used pref. in a list comprehensions
            """
            try:
                if not token.is_punct and not token in self.stopwords:
                    return(token.lemma_)
            except:
                pass

        def _extract_candidates(self, nlpdoc):
            tokens = [self._candidate_token_filter(token) for token in nlpdoc if not self._candidate_token_filter(token) == None]
            return tokens

        def _extract_doc_tokens(self, nlpdoc):
            tokens = [self._doc_token_filter(token) for token in nlpdoc if not self._doc_token_filter(token) == None]
            return tokens

        def _read_data(self, portfolio):
            self.candidate_keywords = []
            self.candidate_keywords_ids = {}
            self.mod_portfolio = []
            self.doc_tokens = []

            for doc in portfolio:
                self.num_docs += 1
                doc = self._doc_normalization(raw_doc = doc)
                doc = self.nlp(doc)

                tokens = self._extract_candidates(nlpdoc = doc)
                doc_tokens = self._extract_doc_tokens(nlpdoc = doc)

                self.doc_tokens.append(doc_tokens)
                self.mod_portfolio.append(' '.join(doc_tokens))

                for word in tokens:
                    if word not in self.stopwords:
                        if word in self.candidate_keywords_ids:
                            next
                        else:
                            cand_id = len(self.candidate_keywords)
                            self.candidate_keywords.append(word)
                            self.candidate_keywords_ids[word] = cand_id

            self.num_candidates = len(self.candidate_keywords)

        def __init__(self, portfolio, stopwords = None, tags = None):

            self.num_docs = 0
            self.docs = []
            self.original_portfolio = portfolio
            self.nlp = spacy.load('en')
            self.tags = tags


            if stopwords == None:
                self.stopwords = nltk.corpus.stopwords.words('english')
            else :
                self.stopwords = stopwords

            self._read_data(portfolio)
            self._build_FreqDist()
            self._build_Ngrams()
            self._build_graph()
            self._build_candidate_degree_weights()
            self._build_candidate_doc_occurence()

        def _build_FreqDist(self):
            """Building frequency distribution over words"""
            self.candidate_freq = nltk.FreqDist([token for tokens in self.doc_tokens for token in tokens])

        def _are_candidates(self, ngram):
            candSet = set(self.candidate_keywords)
            return(all([word in candSet for word in ngram]))

        def _build_Ngrams(self, windowSize = 2):
            """Building Ngrams from all documents """
            docs_Ngrams = [list(nltk.ngrams(doc.rsplit(" "), windowSize)) for doc in self.mod_portfolio]
            self.Ngrams = [Ngram for Ngrams in docs_Ngrams for Ngram in Ngrams if self._are_candidates(Ngram)]
            self.Ngrams_FreqDist = nltk.FreqDist(self.Ngrams)

        def _build_graph(self):
            self.G = nx.Graph()
            self.G.add_nodes_from(self.candidate_keywords)
            self.G.add_edges_from(self.Ngrams)

            for gram in self.Ngrams:
                self.G[gram[0]][gram[1]]["weight"] = self.Ngrams_FreqDist[gram]


        def _build_candidate_degree_weights(self):
            self.degree = self.G.degree()
            self.node_weight = {}
            graph = self.G

            for i, candidate in enumerate(self.G.nodes()):
                node_weights = [graph[candidate][neighbor]["weight"] for neighbor in graph[candidate]]
                self.node_weight[candidate] = sum(node_weights)

        def _build_candidate_doc_occurence(self):
            self.candidate_doc_occur = {}

            for i, candidate in enumerate(self.G.nodes()):
                candidate_inDoc = [1 if candidate in doc else 0 for doc in self.doc_tokens]

                self.candidate_doc_occur[candidate] = sum(candidate_inDoc)


        def sortKeywords(self, ranks):
            """ranks : A dictionary"""
            from operator import itemgetter

            ranks = [items for items in ranks.items()]
            sortRank = sorted(ranks, key =itemgetter(1), reverse=True)
            return(sortRank)


        def extract_keywords_harmonic(self):
            max_edge_weight = max(self.node_weight.values()) # Maximum sum of edge weights among all edges in the graph
            max_degree = max(dict(self.G.degree).values())

            ranks = {cand:hmean([self.G.degree(cand)/max_degree, self.node_weight[cand]/max_edge_weight, self.candidate_doc_occur[cand]/self.num_docs]) for cand in list(self.G.nodes()) if self.G.degree(cand) > 0}
            sortRank = self.sortKeywords(ranks)
            self.ranks_hmean = sortRank
            return(self.ranks_hmean)


        def extract_keywords_pagerank(self):
            return(self.sortKeywords(nx.pagerank(self.G)))

        def extract_keywords_rake(self):
            ranks_rake = {cand: self.degree[cand]/self.candidate_freq[cand] for cand in list(self.G.nodes())}
            self.ranks_rake = self.sortKeywords(ranks_rake)
            return(self.ranks_rake)

        def remove_nodes(self, nodes_to_remove):
            if isinstance(nodes_to_remove, list):
                self.G.remove_nodes_from(nodes_to_remove)
            if isinstance(nodes_to_remove, str):
                self.G.remove_node(nodes_to_remove)

        def getNeighbor(self, node):
            neighbor = {neighbour: self.G[node][neighbour]["weight"] for neighbour in self.G[node]}
            return([node[0] for node in self.sortKeywords(neighbor)])

        def plot_graph(self):
            pass

        def get_summary(self):
            print("Number of Keyword Candidates {}".format(self.num_candidates))
            print("Number of Documents {}".format(self.num_docs))
