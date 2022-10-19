import random
import json
from wordfreq import word_frequency
import math

def histogram(letters):
    """
    Creates a frequency histogram of the given letters
    Input: letters -- word or scrambled letters
    Output: dictionary mapping from letters to the # of occurences of that letter
    """
    d = dict()
    d[0] = len(letters)
    for letter in letters:
        if letter in d:
            d[letter] += 1
        else:
            d[letter] = 1
    return d

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

def unscramble(orig_letters):
    startLetters = ""
    letters = ""
    for letter in orig_letters:
        if letter.upper() == letter:
            startLetters += letter.lower()
        else:
            letters += letter

    possible_words = []
    with open("words_dictionary.json") as json_file:
        # Get words that start with t, i, and w, the capitalized puzzle letters
        words = json.load(json_file)
        for sLetter in startLetters:
            possible_words.append(getCandidates(words, sLetter, letters))

        totalhist = histogram((orig_letters.lower() + (len(startLetters))*" "))

        phrases = dict()

        phrases = unscramble_rec(phrases, possible_words, '', totalhist)

        print( dict(sorted(phrases.items(), key=lambda item: item[1], reverse=True)) )


def unscramble_rec(phrases, possible_words, current_words, totalhist):
    if len(possible_words) > 0:
        for word in possible_words[0]:
            new = current_words + " " + word
            #print(new, histogram(new), totalhist)
            if len(new) <= totalhist[0]:
                phrases = unscramble_rec(phrases, possible_words[1:], new, totalhist)

        return phrases

    elif histogram(current_words) == totalhist:
        phrases[current_words] = 1
        #print(current_words)

    return phrases

if __name__ == '__main__':
    unscramble("SeWhsAeemoAWSeeideeSmoSe")
