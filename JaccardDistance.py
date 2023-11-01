# importing the nltk suite
import nltk

# importing jaccard distance
# and ngrams from nltk.util
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

# Downloading and importing
# package 'words' from nltk corpus
nltk.download('words')
from nltk.corpus import words

# Definir as listas corretas e incorretas como variáveis globais
correct_words = []
incorrect_words = []

# loop for finding correct spellings
# based on jaccard distance

def choose_language(language):
    global correct_words, incorrect_words  # Declare as variáveis como globais
    if language == "es":
        correct_words = words.words('es')
        incorrect_words = ['bannanna', 'lunees', 'tzaa', "ayyr", 'mañaa']
    elif language == "pt":
        correct_words = words.words('pt')
        incorrect_words = ['bannanna', 'seggunda', 'cupo', "omtem", 'noyte']
    elif language == "en":
        correct_words = words.words('en')
        incorrect_words = ['bannanna', 'munday', 'glsas', "yesterdday", 'omrning', 'ikwi']
    else:
        print("Language not supported!")

        
def print_result():
    for word in incorrect_words:
        temp = [(jaccard_distance(set(ngrams(word, 2)),
                                  set(ngrams(w, 2))), w)
                for w in correct_words if w[0] == word[0]]
        print(sorted(temp, key=lambda val: val[0])[0][1])

choose_language("en")
print_result()

# choose_language("es")
# print_result()

# choose_language("pt")
# print_result()
