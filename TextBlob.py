from spellchecker import SpellChecker
from textblob import TextBlob
# from spellchecker import SpellChecker
import re

# incorrect_words = ['pait', 'emgines', 'gera', "reduccer", 'sofmwtwre', 'pinel']
#
# corrected_words = [TextBlob(word).correct() for word in incorrect_words]
#
# print(corrected_words)

# Colocar em outros idiomas
# Tirar do plural

# read dictionary

custom_corrections_file = "dictionary_english.txt"
custom_corrections = {}

with open(custom_corrections_file, "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            incorrect_word, correct_word = parts[0], parts[1]
            custom_corrections[incorrect_word] = correct_word


def clean_text(text):
    # retira os números e coloca em um array
    text = text.lower()
    string = re.findall(r"\b[a-zA-Z]+\b|[,.)('\"\[\];><:\\/@!#$%¨&*_+=]", text)
    print(string)
    return string


def find_errors(text):
    # Encontra as palavras erradas
    spell = SpellChecker()
    misspelled = spell.unknown(text)
    return misspelled


def custom_spell_check(text):
    array = clean_text(text)
    text = text.lower().split(" ")
    print(text)
    wrong_words = find_errors(array)
    corrected_words = []

    for word in text:
        word = re.sub(r'[,.)(\'\"\[\];><:\\/@!#$%¨&*_+=]$', '', word)
        if word in wrong_words:
            # Verifica se a palavra está no dicionário de correções personalizadas
            if word in custom_corrections:
                corrected_word = custom_corrections[word]
            else:
                # Use o TextBlob para correção padrão
                corrected_word = TextBlob(word).correct()
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)

    corrected_text = " ".join([str(word) if isinstance(word, TextBlob) else word for word in corrected_words])
    print(corrected_text)


# Exemplo de uso
input_text = "Air cooleng, engyne. ricce) 'mondai'"
custom_spell_check(input_text)

