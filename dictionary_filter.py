from copy import copy
from typing import Dict, List

from decrypt import create_pattern_equivalents_for_words_in_phrase


def _non_reflective_dictionaries_match(dict1, dict2):
    return all(dict2[key1] == value1 if key1 in dict2 else True for key1, value1 in dict1.items())


def dictionaries_match(dict1, dict2):
    """Checks if some key is in both dictionaries, its values are equal, for every key"""
    return (_non_reflective_dictionaries_match(dict1, dict2) and
            _non_reflective_dictionaries_match(dict2, dict1))


def filter_decryptions_by_dict(dictionary: dict, decryptions: Dict[str, List[Dict[str, str]]]):
    """Removes those decryptions, which do not match (as a dictionary) to given dictionary"""
    filtered_decryptions = copy(decryptions)
    for encrypted_word, word_decryptions in decryptions.items():
        filtered_decryptions[encrypted_word] = [decryption_dict for decryption_dict in word_decryptions if
                                                dictionaries_match(dictionary, decryption_dict)]
    return filtered_decryptions


if __name__ == "__main__":
    assert _non_reflective_dictionaries_match({}, {1: 2})
    assert dictionaries_match({}, {1: 2}) and dictionaries_match({1: 2}, {}) and dictionaries_match({1: 2, 2: 3}, {1: 2, "x": "d"})
    assert not dictionaries_match({1: 2, 2: 3}, {1: 2, 2: 4})
    assert not dictionaries_match({1: 2, 2: 4}, {1: 2, 2: 3})

    encrypted_phrase = "RMJ HLSIZMPS S IRF TSUEZJGSXFPMAQC PFGSEFUSEMVQ"
    possible_decryptions = create_pattern_equivalents_for_words_in_phrase(encrypted_phrase,
                                                                          minimum_occurrences_of_word=20)
    filtered_decryptions = filter_decryptions_by_dict(dict(zip("PFGSEUMSXFPMAQC", "labortiowalismy")), possible_decryptions)
    assert any((len(filtered_decryptions[word]), len(possible_decryptions[word])) for word in encrypted_phrase.split(" "))
