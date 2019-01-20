# ----------
#Example Use
# mySymSpell = symspellpy()
# mySymSpell.init()
# mySymSpell.findSuspiciousWords("this is a test mebmers")
# ----------

import os, re, enchant
from autocorrect import spell


from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

class symspellpy():
    
    # create object
    initial_capacity = 83000
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length)

    dictionary = False
    d = enchant.Dict("en_US")

    def init(self):
        print ("loading dictionary")

        # load dictionary
        dictionary_path = os.path.join("./",
                                       "frequency_dictionary_en_82_765.txt")
        term_index = 0  # column of the term in the dictionary text file
        count_index = 1  # column of the term frequency in the dictionary text file
        if not self.sym_spell.load_dictionary(dictionary_path, term_index, count_index):
            print("Dictionary file not found")
        else:
            print ("dictionary loaded")
            self.dictionary = True
    
    def symspellword(self,word):
        if not self.dictionary:
            return "NO DICTIONARY FOUND"

        # lookup suggestions for single-word input strings
        input_term = word  # misspelling of "members"
        # max edit distance per lookup
        # (max_edit_distance_lookup <= max_edit_distance_dictionary)
        max_edit_distance_lookup = 2
        suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
        suggestions = self.sym_spell.lookup(input_term, suggestion_verbosity,
                                       max_edit_distance_lookup)
        # display suggestion term, term frequency, and edit distance
        for suggestion in suggestions:
            return(suggestion.term)
    
    def symspellphrase(self,text):
        if not self.dictionary:
            return "NO DICTIONARY FOUND"
        # lookup suggestions for multi-word input strings (supports compound
        # splitting & merging)
        input_term = (text)
        # max edit distance per lookup (per single word, not per whole input string)
        max_edit_distance_lookup = 2
        suggestions = self.sym_spell.lookup_compound(input_term,
                                                max_edit_distance_lookup)
        # display suggestion term, edit distance, and term frequency
        for suggestion in suggestions:
            return (suggestion.term)
    

    #really I should run each through a dictionary first, then check for replacements against a dictionary
    #but I don't have much time so I'll just symspell it and check the words that are different
    def findSuspiciousWords(self, text):

        stopwords = ["retweet", "retweeted"]

        try:
            if len(text) < 20:
                print ("Not a text article")
                return []
        except:
            print ("broken text")
            return []

        

        #I'll split this into a bunch of sentences and check each sentence for changes
        sentences = text.split(".")

        bad_words = {}

        for sentence in sentences:
            #pre-process text; remove capital words, remove punctuation
            sentence = sentence.replace("n't", " not")
            sentence = re.sub(r"\[([a-zA-Z]{1})\]", r"\1", sentence)
            sentence = re.sub(r"http\S+", "", sentence)
            sentence = re.sub(r"\S*\.com\S*\s?", "", sentence)
            sentence = re.sub(r"www.\S+", "", sentence)
            sentence = re.sub(r"\S+[@#]\S+", "", sentence)
            sentence = re.sub(r"\S*@\S*\s?", "", sentence)
            
            sentence = re.sub(r'[^\w\s]',' ',sentence)
            sentence = re.sub(r'([A-Z]\w+)', ' ', sentence)
            sentence = re.sub(r'([A-Z])', ' ', sentence)
            sentence = re.sub(r'([0-9])', ' ', sentence)
            sentence = re.sub('\s+', ' ', sentence).strip()
            
            correctedSentence = self.symspellphrase(sentence)
            
            #corrected = self.symspellphrase(text)
            textbroken = sentence.split()
            correctedbroken = correctedSentence.split()

            #print(textbroken)
            #print(correctedbroken)

            for word in textbroken:
                if word not in correctedbroken:
                    try:
                        bad_words[word] +=1
                    except:
                        bad_words[word] = 1

        keys = list(bad_words.keys())
        values = list(bad_words.values())
        
        shadyWords = []
        
        #print ("There are " +str(len(bad_words)) + " questionable words")
        #print (str(values))
        #print (str(keys))
        #print ("Now Checking for False Postives")
        for i in range(len(values)):
            badWord = True
            if values[i] == 1:
            
                correctedWord = spell(keys[i])
                
                if keys[i] in stopwords:
                    badWord = False
                
                if correctedWord == keys[i]:
                    badWord = False

                elif len(keys[i]) < 3:
                    badWord = False
                
                elif self.d.check(keys[i]):
                    badWord = False
                    
                elif keys[i].endswith("n"):
                    if self.d.check(keys[i][:-1]):
                        badWord = False

                if badWord:
                    shadyWords.append(keys[i])
                        
        badWordDict = {}
        for word in shadyWords:
            print (word + " is a bad word in ")
            for sentence in sentences:
                if word in sentence:
                    badWordDict[word] = sentence
                    print(sentence)
                    print("")
                    
        print ("Done Spell Checking")
                    
        return badWordDict



