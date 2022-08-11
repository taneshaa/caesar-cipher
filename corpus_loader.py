import ssl
import nltk  # Will need to pip install nltk


nltk.download("words", quiet=True)
nltk.download("names", quiet=True)

from nltk.corpus import words, names
word_list = words.words()
name_list = names.words()
