from collections import defaultdict
from os.path import isfile


def find_ngrams(default_path=None, *, n: int=1) -> str:
    """Find file with n-grams"""
    if default_path is None:
        if isfile("{}grams".format(n)):
            return "{}grams".format(n)
    else:
        if isfile(default_path):
            return default_path

    path = ""
    while not isfile(path):
        print("Pobierz plik {}grams.gz".format(n),
              "http://zil.ipipan.waw.pl/NKJPNGrams",
              "rozpakuj i podaj ścieżkę do pliku {}grams".format(n), sep="\n")
        path = input().rstrip("\n").strip('"')
    return path


def load_unigrams(*, minimum_occurrences_of_word=50, unigrams_path="1grams"):
    """Loads unigrams with number of occurences greater than minimum from file"""
    path = find_ngrams(unigrams_path)
    unigrams = defaultdict(lambda: {})
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            count, word = line.strip().split(" ")
            if int(count) < minimum_occurrences_of_word:
                break
            if word.isalpha():
                unigrams[len(word)][word] = int(count)
    return unigrams

if __name__ == "__main__":
    unigrams = load_unigrams(minimum_occurrences_of_word=5000000)
    assert all(count >= 5000000 for given_length_unigrams in unigrams.values() for count in given_length_unigrams.values())