import math
import argparse
import codecs
import operator
from collections import defaultdict
import random

"""
This file is part of the computer assignments for the course DD1418/DD2418 Language engineering at KTH.
Created 2018 by Johan Boye and Patrik Jonell.
"""

class Generator(object) :
    """
    This class generates words from a language model.
    """
    def __init__(self):
    
        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = {}

        # The bigram log-probabilities.
        self.bigram_prob = defaultdict(dict)

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        # The average log-probability (= the estimation of the entropy) of the test corpus.
        # Important that it is named self.logProb for the --check flag to work
        self.logProb = 0

        # The identifier of the previous word processed in the test corpus. Is -1 if the last word was unknown.
        self.last_index = -1

        # The fraction of the probability mass given to unknown words.
        self.lambda3 = 0.000001

        # The fraction of the probability mass given to unigram probabilities.
        self.lambda2 = 0.01 - self.lambda3

        # The fraction of the probability mass given to bigram probabilities.
        self.lambda1 = 0.99

        # The number of words processed in the test corpus.
        self.test_words_processed = 0


    def read_model(self,filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                curLine = 0
                for row in f.readlines():
                    curRow = row.strip().split(' ')
                    if curRow == ["-1"]:
                        pass
                    elif curLine < self.unique_words:
                        self.word[curRow[0]] = curRow[1]
                        self.index[curRow[1]] = curRow[0]
                        self.unigram_count[1] = curRow[2]
                    else:
                        self.bigram_prob [curRow[0]][curRow[1]] = curRow[2]

                    curLine += 1
                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def generate(self, w, n):

        self.last_index = self.index[w]
        outPut = w
        numOfWords = 0
        while numOfWords < n:
            words = []
            distribution = []
            for secondWord in self.bigram_prob[self.last_index]:
                logP = self.bigram_prob[self.last_index][secondWord]
                probability = math.exp(float(logP))
                words.append(self.word[secondWord])
                distribution.append(probability)

            if not words:
                indexChosenWord = str(max(self.unigram_count.items(), key=operator.itemgetter(1))[0])
                chosenWord = self.word[indexChosenWord]
            else:
                chosenWord = (random.choices(words, distribution))
                chosenWord = chosenWord[0]

            outPut += ' '+chosenWord
            self.last_index = self.index[chosenWord]
            numOfWords += 1

        print(outPut)

#python Generator.py -f small_model.txt -s i

def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--start', '-s', type=str, required=True, help='starting word')
    parser.add_argument('--number_of_words', '-n', type=int, default=100)

    arguments = parser.parse_args()

    generator = Generator()
    generator.read_model(arguments.file)
    generator.generate(arguments.start, arguments.number_of_words)

if __name__ == "__main__":
    main()
