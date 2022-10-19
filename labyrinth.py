import random
import json
from wordfreq import word_frequency
import math

minotaur = "minotaur"
letters = "ashencneton"
startletters = "tiw"

def histogram(letters):
    """
    Creates a frequency histogram of the given letters
    Input: letters -- word or scrambled letters
    Output: dictionary mapping from letters to the # of occurences of that letter
    """
    d = dict()
    for letter in letters:
        if letter in d:
            d[letter] += 1
        else:
            d[letter] = 1
    return d

letterhist = histogram(letters)

def isSubhist(hist1, hist2):
    """
    Checks if hist1 is a subset of hist2
    Input: hist1, hist2 -- dictionary histograms
    Output: Boolean
    """
    for letter in hist1:
        if letter not in hist2 or hist1[letter] > hist2[letter]:
            return False
    return True

def getWordsStartWith(words, start):
    """
    Returns the subset of words that start with the letter "start"
    Input: words -- set, dict, or list of words
           start -- starting character
    Output: Set of words starting with "start"
    """
    return set([word for word in words if word[0] == start])


def getCandidates(all_words, start, letters):
    """
    Finds words that could be created with the given letters
    Input: all_words -- set, dict, or list of words
           start -- starting character
           letters -- scrambled letters to make words from
    Output: Set of words starting with "start", and containing only "letters"
    """
    words = getWordsStartWith(all_words, start)
    available = histogram(letters + start)

    candidates = set()
    for word in words:
        if isSubhist(histogram(word), available):
            candidates.add(word)
    return candidates

def main():
    """
    create phrases with only the given global "letters" and rank according to usage frequency
    """
    words = {}
    # Opening JSON file
    with open("words_dictionary.json") as json_file:
        # Get words that start with t, i, and w, the capitalized puzzle letters
        words = json.load(json_file)
        t_words = getCandidates(words, "t", letters)
        i_words = getCandidates(words, "i", letters)
        w_words = getCandidates(words, "w", letters)
        m_words = getCandidates(words, "m", letters)

        print(t_words, len(t_words))
        print(i_words, len(i_words))
        print(w_words, len(w_words))
        print(m_words, len(m_words))

        totalhist = histogram(letters + "tiw")

        phrases = dict()
        for t in t_words:
            for i in i_words:
                for w in w_words:
                    if (histogram(t+i+w) == totalhist):
                        phrase = (t+" "+i+" "+w)
                        phrase += " "+minotaur

                        wf = word_frequency(t, "en", wordlist='small', minimum=0.0) * \
                         word_frequency(i, "en", wordlist='small', minimum=0.0) * \
                         word_frequency(w, "en", wordlist='small', minimum=0.0)

                        phrases[phrase] = wf

        print( dict(sorted(phrases.items(), key=lambda item: item[1], reverse=True)) )
        print(len(phrases))
if __name__ == '__main__':
    main()
    #unscramble("SeWhsAeemoAWSeeideeSmoSe")
