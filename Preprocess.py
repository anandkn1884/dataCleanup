import os
import inflect
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import reader
from nltk.stem import PorterStemmer

p = inflect.engine()
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

dataPath = "<path_to_folder>"

contractions = { 
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that had",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there had",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they had",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

def substitute_contractions(line):
    for k,v in contractions.items():
        line = re.sub(k, v, line)
    return line

# Function to check if a string is a number.
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


fileList = os.listdir(dataPath) # Read files from a given path one by one.
for f in fileList:  
    with open(dataPath + "/" + f, "r", encoding='UTF-8') as ins:
        for line in ins: # Read lines from each file.

            line = re.sub('\s+', " ", line) # Substitute white spaces in each line. 

            line = re.sub('\s+(\')', "'", line) # Substitute white spaces before apostrophes. 
            
            line = substitute_contractions(line) # Substitute contractions in each line. 
                
            words = word_tokenize(line) # Tokenize the sentences in each line.
            newline = ""
            for word in words:
                if(any(char.isdigit() for char in word)):
                    number_letter = re.findall(r'[A-Za-z]+|\d+', word) # Separate Numbers and letters. 60m to 60 m. 
                    for nl in number_letter:
                        newline = newline + " " + nl.lower()    # Convert words to lower case.
                else:
                    newline = newline + " " + word.lower() # Convert words to lower case.
            newline_numbersSeparated = newline
            
            words = word_tokenize(newline)
            newline = ""
            for word in words:
                if word in stop_words: # Remove Stop words.
                    continue
                if(is_number(word)):
                    newline = newline + " " + p.number_to_words(word) # Convert all numerals to word equivalent. 65 to Sixty Five.
                else:
                    newline = newline + " " + ps.stem(word)    # Stem the words using Porter Stemmer.
            newline_Stemmed_WithoutStopWords = newline