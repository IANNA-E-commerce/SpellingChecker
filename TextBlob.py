from spellchecker import SpellChecker
from textblob import TextBlob
import re

custom_corrections_file = "dictionary_english.txt"
custom_corrections = {}
index_word = 1
corrected_words = []

with open(custom_corrections_file, "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            incorrect_word, correct_word = parts[0], parts[1]
            custom_corrections[incorrect_word] = correct_word


def clean_text(text):
    # create a new string without numbers and other symbols
    string = re.findall(r"\b[a-zA-Z0-9]+\b|[,.)('\"\[\];><:\\/@!#$%¨&*_+=]", text)
    return string


def find_errors(text):
    # Find the wrong words
    spell = SpellChecker()
    misspelled = spell.unknown(text)
    return misspelled


def separate_word(word, index):
    return [word[:index], word[index:]]


def return_custom_corrections(word):
    if word in custom_corrections:
        return custom_corrections[word]


def return_textblob_correction(word):
    if len(find_errors([word])) == 0:
        return word
    corrected_word = TextBlob(word).correct()
    if corrected_word != word:
        return corrected_word
    # return False


def find_words(word):
    for index in range(len(word)):
        separate_words = separate_word(word, (index + 1))
        if len(find_errors(separate_words)) == 0:
            corrected_words.append(separate_words[0])
            corrected_words.append(separate_words[1])
            return True
    for index in range(len(word)):
        separate_words = separate_word(word, (index + 1))
        if return_custom_corrections(separate_words[0]):
            if return_custom_corrections(separate_words[1]):
                corrected_words.append(return_custom_corrections(separate_words[0]))
                corrected_words.append(return_custom_corrections(separate_words[1]))
                return True
            elif return_textblob_correction(separate_words[1]):
                corrected_words.append(return_custom_corrections(separate_words[0]))
                corrected_words.append(return_textblob_correction(separate_words[1]))
                return True
        elif return_textblob_correction(separate_words[0]):
            if return_custom_corrections(separate_words[1]):
                corrected_words.append(return_textblob_correction(separate_words[0]))
                corrected_words.append(return_custom_corrections(separate_words[1]))
                return True
            elif return_textblob_correction(separate_words[1]):
                corrected_words.append(return_textblob_correction(separate_words[0]))
                corrected_words.append(return_textblob_correction(separate_words[1]))
                return True
    return False


def verification_correction(text):
    global index_word
    array = clean_text(text)
    wrong_words = find_errors(array)

    if index_word == -1:
        return corrected_words

    # Give preference for words in our dictionary
    for word in array:
        if word in wrong_words:
            # Verifica se a palavra está no dicionário de correções personalizadas
            if not return_custom_corrections(word):
                # Use o TextBlob para correção padrão
                if not return_textblob_correction(word):
                    if not find_words(word):
                        print("Não descobriu uma palavra")
                else:
                    corrected_words.append(return_textblob_correction(word))
            else:
                corrected_words.append(return_custom_corrections(word))
        else:
            corrected_words.append(word)


def custom_spell_check(text):
    text = text.lower()
    verification_correction(text)

    corrected_text = ""
    if corrected_words is not None:
        for word in corrected_words:
            if isinstance(word, TextBlob):
                corrected_text += " " + str(word)
            elif word.isnumeric() or word.isalpha():
                corrected_text += " " + str(word)
            else:
                corrected_text += word

    print(corrected_text)
    return corrected_text


input_text = "yo soy hermano"
custom_spell_check(input_text)
