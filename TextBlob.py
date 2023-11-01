from spellchecker import SpellChecker
from textblob import TextBlob
import re

# Colocar em outros idiomas
# Tirar do plural

custom_corrections_file = "dictionary_english.txt"
custom_corrections = {}
index_word = 1

with open(custom_corrections_file, "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            incorrect_word, correct_word = parts[0], parts[1]
            custom_corrections[incorrect_word] = correct_word


def clean_text(text):
    # create a new string without numbers and other symbols
    string = re.findall(r"\b[a-zA-Z0-9]+\b|[,.)('\"\[\];><:\\/@!#$%¨&*_+=]", text)
    print("string = ", string)
    # it modifies the original text for an array
    # text = text.split(" ")
    return string


def find_errors(text):
    # Find the wrong words
    spell = SpellChecker()
    misspelled = spell.unknown(text)
    return misspelled


def correct_text_blob(word):
    global index_word
    corrected_word = TextBlob(word).correct()
    if corrected_word == TextBlob(word).correct() and len(word) > 1:
        separate_words = word[:index_word] + " " + word[index_word:]
        print("separate_words", separate_words)
        custom_spell_check(separate_words)
        index_word = index_word + 1
    else:
        return corrected_word


def separate_word(word, index):
    return word[:index] + " " + word[index:]


def custom_spell_check(text):
    global index_word
    text = text.lower()
    print("text1 = ", text)
    array = clean_text(text)
    wrong_words = find_errors(array)
    print("wrong_words = ", wrong_words)
    corrected_words = []

    # Give preference for words in our dictionary
    for word in array:
        if word in wrong_words:
            # Verifica se a palavra está no dicionário de correções personalizadas
            if word in custom_corrections:
                corrected_word = custom_corrections[word]
            else:
                # Use o TextBlob para correção padrão
                corrected_word = TextBlob(word).correct()
                if corrected_word == word:
                    if index_word < len(word):
                        separate_words = separate_word(word, index_word)
                        print("separate_words = ", separate_words)
                        index_word = index_word + 1
                        corrected_word = custom_spell_check(separate_words)

            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)

    corrected_text = ""
    print(corrected_words)
    for word in corrected_words:
        if isinstance(word, TextBlob):
            corrected_text += " " + str(word)
        elif word.isnumeric() or word.isalpha():
            corrected_text += " " + str(word)
        else:
            corrected_text += word

    print(corrected_text)
    return corrected_text


# Exemplo de uso
input_text = "speelingchecker"
custom_spell_check(input_text)
