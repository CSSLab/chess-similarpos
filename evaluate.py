import encoding
from rank_bm25 import BM25Okapi

def top_n_most_similar(query, samples, top_n):

  corpus = list(map(encoding.get_encoding, samples))

  tokenized_corpus = [doc.split(" ") for doc in corpus]
  bm25 = BM25Okapi(tokenized_corpus)

  q = encoding.get_encoding(query)
  tokenized_query = q.split(" ")

  ranking = bm25.get_top_n(tokenized_query, corpus, n=top_n)

  return [samples[corpus.index(i)] for i in ranking]