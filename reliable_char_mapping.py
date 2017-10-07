from typing import List, Dict
from copy import copy, deepcopy

from decrypt import create_pattern_equivalents_for_words_in_phrase
from dictionary_filter import dictionaries_match, filter_decryptions_by_dict


def reliable_mapping(possible_decryptions) -> Dict[str, str]:
    """Selects characters, such that, in every possible decryption, this character is mapped to the same letter"""
    certain_chars = {}
    for char in possible_decryptions[0].keys():
        if len(set(d[char] for d in possible_decryptions)) == 1:
            certain_chars[char] = possible_decryptions[0][char]
    return certain_chars


def select_decryptions_matching_reliable_chars(encrypted_phrase, possible_decryptions: Dict[str, List[Dict[str, str]]]):
    """Uses reliable char mapping to limit quantity of possible decryptions
    as long as those number of those decryptions decreases"""
    previous_certain_chars = [None]
    certain_chars: List[Dict[str, str]] = [{}]
    decryptions = copy(possible_decryptions)

    while certain_chars[0] != previous_certain_chars[0]:
        previous_certain_chars = deepcopy(certain_chars)
        for encrypted_word in possible_decryptions.keys():
            certain_chars.append(reliable_mapping(decryptions[encrypted_word]))

        while len(certain_chars) > 1:
            assert dictionaries_match(certain_chars[0], certain_chars[-1])
            certain_chars[0].update(certain_chars[-1])
            certain_chars.pop()

        decryptions = filter_decryptions_by_dict(certain_chars[0], decryptions)
    return decryptions


if __name__ == "__main__":
    assert reliable_mapping(
        [dict(zip("PFGSEFUSEMVQ", "laboratorium")),
         dict(zip("PFGSEFUSEMVQ", "laboratoriów"))]) == dict(zip("PFGSEUM", "laborti"))

    encrypted_phrase = "RMJ HLSIZMPS S IRF TSUEZJGSXFPMAQC PFGSEFUSEMVQ"
    possible_decryptions = create_pattern_equivalents_for_words_in_phrase(encrypted_phrase,
                                                                          minimum_occurrences_of_word=20)
    assert len(possible_decryptions["TSUEZJGSXFPMAQC"]) > 1 and len(possible_decryptions["PFGSEFUSEMVQ"]) > 1
    possible_decryptions = select_decryptions_matching_reliable_chars(encrypted_phrase, possible_decryptions)
    assert len(possible_decryptions["TSUEZJGSXFPMAQC"]) == 1 and len(possible_decryptions["PFGSEFUSEMVQ"]) == 1
