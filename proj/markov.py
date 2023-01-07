import hashtable
import math
import pytest
import pathlib

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2
def kgenerator(string, k, form):
    """
    Function for generating k and k+1 strings for a k-order markov model.

    Paramters:
        - String (str): string to process and create k and k+1 strings from
        - k (int): length of strings to create
        - form (bool): Determines form of output. True = output as list of k and k+1 strings,
          False =  output as list of tuples of k and k+1 (e.g., (k, k+1))
    
    Output:
        either a list of strings, or a list of tuples of k and k+1 length
    """
    output = [ ]

    #lengthening string to support wrap around
    test_string = string + string[:k*2]
    
    if form:
        for i in range(len(string)):
            output.append(test_string[i:i+k])
            output.append(test_string[i:i+k+1])
        return output
    else:
        for i in range(len(string)):
            k_string = test_string[i:i+k]
            k1_string = test_string[i:i+k+1]
            output.append((k_string, k1_string))
        return output

class Markov:
    def __init__(self, k, text, use_hashtable=True):
        """
        Construct a new k-order markov model using the text 'text'.

        Parameters:
        self.k: k order of markov model
        self.text: text to build model on
        self.use_hashtable: boolean value indicating whether model should use dict or custom hashtable

        additional attributes:
        self.h: label for dict or hashtable in use
        self.unique_ch: number of unique characters in self.text for laplace smoothing
        """
        self.k = k
        self.text = text
        self.use_hashtable = use_hashtable

        if self.use_hashtable:
            self.h = hashtable.Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            self.h = { }
        
        k_strings = kgenerator(self.text, self.k, True)

    
        for string in k_strings:
            if string in self.h:
                self.h[string] += 1
            else:
                self.h[string] = 1
        
        #identifying unique characters in text for laplace smoothing
        self.unique_ch = len(set(self.text))


    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """

        test_kstrings = kgenerator(s, self.k, False)

        total = 0

        for tup in test_kstrings:

            #if-else structure to handle differences in hashtable and dict implementations
            #hashtable always returns true for "in" because of default value
            if tup[1] in self.h:
                m = self.h[tup[1]]
            else:
                m = 0
            
            if tup[0] in self.h:
                n = self.h[tup[0]] 
            else:
                n = 0
            
            total = total + math.log((m + 1)/(n + self.unique_ch))
        
        return total

    




def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """

    speaker1 = Markov(k, speech1, use_hashtable)
    speaker2 = Markov(k, speech2, use_hashtable)


    #normalizing log probabilities
    log1 = speaker1.log_probability(speech3)/len(speech3)
    log2 = speaker2.log_probability(speech3)/len(speech3)

    if log1 >= log2:
        return (log1, log2, "A")
    else:
        return (log1, log2, "B")



