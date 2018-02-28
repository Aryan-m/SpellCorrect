import math, collections
class CustomModel:

  def __init__(self, corpus):
    """Initial custom language model and structures needed by this mode"""
    self.counts = collections.defaultdict(lambda: 0)
    self.bigrams = collections.defaultdict(lambda:0)
    self.unigrams = collections.defaultdict(lambda:0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
    """
    # TODO your code here
    preWord = 'NULL'
    word = '<s>'
    postWord = 'NULL'

    for sentence in corpus.corpus:
      for datum in sentence.data:
        postWord = datum.word
        if preWord != 'NULL':
          self.counts[(preWord, word, postWord)] += 1
        self.bigrams[(word, postWord)] += 1
        self.unigrams[postWord] += 1
        preWord = word
        word = postWord
        self.total += 1
      self.unigrams['<s>'] += 1
      self.counts[(preWord, word, '</s>')] += 1
      self.bigrams[(word, '</s>')] += 1
      self.unigrams['</s>'] += 1
      self.total += 2
      preWord = 'NULL'
      word = '<s>'
      postWord = 'NULL'

  def score(self, sentence):
    """ With list of strings, return the log-probability of the sentence with language model. Use
        information generated from train.
    """
    # TODO your code here
    score = 0.0
    preWord = 'NULL'
    word = '<s>'
    postWord = 'NULL'

    for token in sentence:
      #set up counts
      postWord = token
      count = self.unigrams[word]
      triCount = self.counts[(preWord, word, postWord)]
      biCount = self.bigrams[(word, postWord)]

      # trigram exists
      if triCount > 0:
        score += math.log(triCount)
        score -= math.log(self.bigrams[(preWord, word)])
      # trigram doesn't exist but bigram does
      if triCount <= 0 and biCount > 0:
        score += math.log(0.4 * biCount)
        score -= math.log(self.unigrams[word])
      # neither bigram nor trigram exist, use unigram
      if triCount <= 0 and biCount <= 0:
        score += math.log(0.4 * (self.unigrams[postWord] + 1))
        score -= math.log(self.total + (len(self.unigrams)))

      preWord = word
      word = postWord

    triCount = self.counts[(preWord, word, '</s>')]
    biCount = self.bigrams[(word, '</s>')]
    count = self.unigrams['</s>']

    # trigram exists
    if triCount > 0:
      score += math.log(triCount)
      score -= math.log(self.bigrams[(word, '</s>')])
    # trigram doesn't exist but bigram does
    if triCount <= 0 and biCount > 0:
      score += math.log(0.4 * biCount)
      score -= math.log(self.unigrams[word])
    # neither bigram nor trigram exist, use unigram
    if triCount <= 0 and biCount <= 0:
      score += math.log(0.4 * (count + 1))
      score -= math.log(self.total + (len(self.unigrams)))

    return score
