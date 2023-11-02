from spellchecker import SpellChecker
from textblob import TextBlob
import re

# Colocar em outros idiomas
# Tirar do plural

custom_corrections_file = "dictionary_english.txt"
custom_corrections = {}
index_word = 1
ver_true = [True, True]
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
    return corrected_word
    # if corrected_word == TextBlob(word).correct() and len(word) > 1:
    #     separate_words = word[:index_word] + " " + word[index_word:]
    #     print("separate_words", separate_words)
    #     custom_spell_check(separate_words)
    #     index_word = index_word + 1
    # else:
    #     return corrected_word


def separate_word(word, index):
    # return word[:index] + " " + word[index:]
    return [word[:index], word[index:]]


def logic_ver_true():
    global ver_true
    global index_word
    if ver_true == [False, False]:
        ver_true = [True, False]
    elif ver_true == [True, False]:
        ver_true = [True, True]
    else:
        index_word = -1


def correcao_personalizada(word):
    if word in custom_corrections:
        corrected_words.append(custom_corrections[word])
        logic_ver_true()
        return True
    return False


def correcao_padrao(word):
    corrected_word = TextBlob(word).correct()
    if corrected_word != word:
        corrected_words.append(corrected_word)
        return True
    return False


def descobrir_palavras(word):
    for index in range(len(word)):
        separate_words = separate_word(word, index)
        # print("Palavras corretas ", separate_words)
        # print("Find Errors ", find_errors(separate_words))
        if len(find_errors(separate_words)) == 0:
        # errors = find_errors(separate_words[0] + " " + separate_words[1])
        # print(errors)
        # print(correct_text_blob(separate_words[0]))
        # print(correct_text_blob(separate_words[1]))
            print("Palavras corretas IF ", separate_words)
            corrected_words.append(separate_words[0])
            corrected_words.append(separate_words[1])
            return True
    for index in range(len(word)):
        separate_words = separate_word(word, index)
        print("Palavras corrigidas ", separate_words)
        if correcao_personalizada(separate_words[0]) or correcao_padrao(separate_words[0]):
            if correcao_personalizada(separate_words[1]) or correcao_padrao(separate_words[1]):
                print("Palavras corrigidas IF ", separate_words)
                corrected_words.append(separate_words[0])
                corrected_words.append(separate_words[1])
                return True
    return False


def verification_correction(text):
    global index_word
    global ver_true
    print("text1 = ", text)
    array = clean_text(text)
    print("array = ", array)
    wrong_words = find_errors(array)

    print("wrong_words = ", wrong_words)
    if ver_true == [True, True] and index_word == -1:
        print("verif")
        return corrected_words

    # Give preference for words in our dictionary
    for word in array:
        if word in wrong_words:
            # Verifica se a palavra está no dicionário de correções personalizadas
            if not correcao_personalizada(word):
                # Use o TextBlob para correção padrão
                if not correcao_padrao(word):
                    if not descobrir_palavras(word):
                        print("Não descobriu uma palavra")
                        # verification_correction(separate_words)
                        corrected_words.append(word)
                        # logic_ver_true()
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


# Use examples
input_text = " lyke paintengyne"
custom_spell_check(input_text)
