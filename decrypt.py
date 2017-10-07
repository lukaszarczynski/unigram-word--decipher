from typing import List, Dict
from collections import defaultdict

from pattern_equivalence import remove_polish_characters, pattern_equivalence
from unigrams import load_unigrams


def find_pattern_equivalent_words(encrypted_word, unigrams) -> List[Dict[str, str]]:
    """Finds words which are pattern equivalent to given word"""
    possible_word_decryptions = []
    encrypted_pattern_equivalence = pattern_equivalence(encrypted_word)
    for word in unigrams[len(encrypted_word)].keys():
        if encrypted_pattern_equivalence(word):
            possible_decryption = dict(zip(encrypted_word, remove_polish_characters(word)))
            if possible_decryption not in possible_word_decryptions:
                possible_word_decryptions.append(dict(zip(encrypted_word, remove_polish_characters(word))))
    return possible_word_decryptions


def create_pattern_equivalents_for_words_in_phrase(encrypted_phrase,
                                                   minimum_occurrences_of_word=50) -> Dict[str, List[Dict[str, str]]]:
    """Creates lists of pattern equivalent words for each word in given phrase"""
    unigrams = load_unigrams(minimum_occurrences_of_word=minimum_occurrences_of_word)
    possible_decryptions = defaultdict(lambda: [])

    for encrypted_word in encrypted_phrase.split(" "):
        pattern_equivalent_words = find_pattern_equivalent_words(encrypted_word, unigrams)
        if len(pattern_equivalent_words) > 0:
            possible_decryptions[encrypted_word] = pattern_equivalent_words
    return possible_decryptions


def decrypt_with_given_dictionary(encrypted_word, decryption_dictionary):
    """Decrypts word using decryption dictionary"""
    return "".join([decryption_dictionary.get(char, "?") for char in encrypted_word])


if __name__ == "__main__":
    unigrams = load_unigrams()
    xddd_equivalents = find_pattern_equivalent_words("xddd", unigrams)
    assert any(decryption_dict == {"x": "h", "d": "m"} for decryption_dict in xddd_equivalents)
    phrase_equivalents = create_pattern_equivalents_for_words_in_phrase("lorem ipsum xddd")
    assert phrase_equivalents["xddd"] == xddd_equivalents
    decryption_dict = dict(zip("abc", "qwe"))
    assert (decrypt_with_given_dictionary("qc", decryption_dict) == "?e" and
            decrypt_with_given_dictionary("baba", decryption_dict) == "wqwq")