import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigrams = collections.defaultdict(lambda:0)
    self.bigrams = collections.defaultdict(lambda:0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    word = 'NULL'
    preWord = '<s>'
    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        self.unigrams[word] += 1
        self.bigrams[(preWord, word)] += 1
        preWord = datum.word
        self.total += 1
      self.unigrams['<s>'] += 1
      self.unigrams['</s>'] += 1
      self.bigrams[(word, '</s>')] += 1
      self.total += 2

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    word = 'NULL'
    preWord = '<s>'
    for token in sentence:
      word = token
      count = self.bigrams[(preWord, word)]
      # bigram exists
      if count > 0:
        score += math.log(count)
        score -= math.log(self.unigrams[preWord])
      # bigram doesn't exist, use unigram
      else:
        score += math.log(0.4 * (self.unigrams[word] + 1))
        score -= math.log(self.total + (len(self.unigrams)))
      preWord = token

    count = self.bigrams[(preWord, '</s>')]
    # bigram exists
    if count > 0:
      score += math.log(count)
      score -= math.log(self.unigrams[preWord])
    # bigram doesn't exist, use unigram
    else:
      score += math.log(0.4 * (self.unigrams['</s>'] + 1))
      score -= math.log(self.total + (len(self.unigrams)))

    return score
