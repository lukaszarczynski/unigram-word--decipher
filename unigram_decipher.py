from collections import defaultdict
from copy import copy

DEBUG = True

def load_unigrams(unigrams_path="1grams"):
    unigrams = defaultdict(lambda: {})
    with open(unigrams_path, encoding="utf-8") as file:
        for line in file:
            count, word = line.strip().split(" ")
            if int(count) < 10:
                break
            if word.isalpha():
                unigrams[len(word)][word] = count
    return unigrams


def same_letters_indices(word):
    same_letters = []
    for idx, letter in enumerate(word):
        for another_idx, another_letter in enumerate(word):
            if letter == another_letter and idx < another_idx:
                same_letters.append((idx, another_idx))
    if DEBUG:
        print(same_letters)
    return same_letters


def remove_polish_characters(word):
    polish_characters = dict(zip("ęóąśłżźćń", "eoaslzzcn"))
    word = [polish_characters.get(char, char) for char in word]
    return "".join(word)


def equal_words(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    return remove_polish_characters(word1) == remove_polish_characters(word2)


def same_letters_match(word, same_letters):
    return all(equal_words(word[idx1], word[idx2]) for idx1, idx2 in same_letters)


def different_letters_match(word, same_letters):
    letters_match = True
    for idx1, letter1 in enumerate(word):
        for idx2, letter2 in enumerate(word):
            if idx1 < idx2 and (idx1, idx2) not in same_letters and word[idx1] == word[idx2]:
                letters_match = False
    return letters_match


def pattern_equivalence(word1):
    same_letters_1 = same_letters_indices(word1)

    def first_word_pattern_equivalence(word2):
        if same_letters_match(word2, same_letters_1) and different_letters_match(word2, same_letters_1):
            return True
        return False

    return first_word_pattern_equivalence


unigrams = load_unigrams()
encrypted_phrase = input().rstrip().split(" ")

possible_decryptions = defaultdict(lambda: [])

for encrypted_word in encrypted_phrase:
    encrypted_pattern_equivalence = pattern_equivalence(encrypted_word)
    for word in unigrams[len(encrypted_word)].keys():
        if encrypted_pattern_equivalence(word):
            possible_decryptions[encrypted_word].append((word, dict(zip(encrypted_word, remove_polish_characters(word)))))
    print(possible_decryptions[encrypted_word])
