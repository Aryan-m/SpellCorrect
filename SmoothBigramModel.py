import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.counts = collections.defaultdict(lambda: 0)
    self.words = collections.defaultdict(lambda:0)
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
        self.words[preWord] += 1
        self.counts[(preWord, word)] += 1
        preWord = datum.word
      self.words['</s>'] += 1
      self.counts[(word, '</s>')] += 1
      preWord = '<s>'


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
      count = self.counts[(preWord, word)]
      score += math.log(count + 1)
      score -= math.log(self.words[preWord] + len(self.words))
      preWord = token

    count = self.counts[(preWord, '</s>')]
    score += math.log(count + 1)
    score -= math.log(self.words[preWord] + len(self.words))
    return score