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
    print("wrong_words", misspelled)
    return misspelled


def separate_word(word, index):
    return [word[:index], word[index:]]


def correcao_personalizada(word):
    if word in custom_corrections:
        return custom_corrections[word]


def correcao_padrao(word):
    if len(find_errors([word])) == 0:
        return word
    corrected_word = TextBlob(word).correct()
    if corrected_word != word:
        return corrected_word
    # return False


def descobrir_palavras(word):
    print(word)
    for index in range(len(word)):
        separate_words = separate_word(word, (index + 1))
        if len(find_errors(separate_words)) == 0:
            corrected_words.append(separate_words[0])
            corrected_words.append(separate_words[1])
            return True
    for index in range(len(word)):
        separate_words = separate_word(word, (index + 1))
        print("Palavras corrigidas ", separate_words)
        if correcao_personalizada(separate_words[0]):
            if correcao_personalizada(separate_words[1]):
                corrected_words.append(correcao_personalizada(separate_words[0]))
                corrected_words.append(correcao_personalizada(separate_words[1]))
                return True
            elif correcao_padrao(separate_words[1]):
                corrected_words.append(correcao_personalizada(separate_words[0]))
                corrected_words.append(correcao_padrao(separate_words[1]))
                return True
        elif correcao_padrao(separate_words[0]):
            if correcao_personalizada(separate_words[1]):
                corrected_words.append(correcao_padrao(separate_words[0]))
                corrected_words.append(correcao_personalizada(separate_words[1]))
                return True
            elif correcao_padrao(separate_words[1]):
                corrected_words.append(correcao_padrao(separate_words[0]))
                corrected_words.append(correcao_padrao(separate_words[1]))
                return True
    return False


def verification_correction(text):
    global index_word
    array = clean_text(text)
    wrong_words = find_errors(array)

    if index_word == -1:
        print("verif")
        return corrected_words

    # Give preference for words in our dictionary
    for word in array:
        print("word", word)
        if word in wrong_words:
            # Verifica se a palavra está no dicionário de correções personalizadas
            if not correcao_personalizada(word):
                # Use o TextBlob para correção padrão
                if not correcao_padrao(word):
                    if not descobrir_palavras(word):
                        print("Não descobriu uma palavra")
                else:
                    corrected_words.append(correcao_padrao(word))
            else:
                corrected_words.append(correcao_personalizada(word))
        else:
            corrected_words.append(word)
            # logic_ver_true()


def custom_spell_check(text):
    text = text.lower()
    verification_correction(text)

    corrected_text = ""
    print("corrected_words = ", corrected_words)
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


input_text = "motorengyne"
custom_spell_check(input_text)
