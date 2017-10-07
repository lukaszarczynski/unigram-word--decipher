from decrypt import create_pattern_equivalents_for_words_in_phrase, decrypt_with_given_dictionary
from partial_decryption_tree import PartialDecryptionTree
from reliable_char_mapping import select_decryptions_matching_reliable_chars, reliable_mapping


MINIMUM_OCCURENCES_OF_WORD = 100


def print_possible_decryptions(encrypted_phrase, possible_decryptions):
    for encrypted_word in encrypted_phrase.split(" "):
        print([(decrypt_with_given_dictionary(encrypted_word, decryption_dict), decryption_dict)
               for decryption_dict in possible_decryptions[encrypted_word]])
        print(reliable_mapping(possible_decryptions[encrypted_word]), "\n")


if __name__ == "__main__":
    print("Wpisz zakodowany tekst:")
    encrypted_phrase = input().rstrip().upper()

    possible_decryptions = create_pattern_equivalents_for_words_in_phrase(encrypted_phrase,
                                                                          minimum_occurrences_of_word=MINIMUM_OCCURENCES_OF_WORD)
    possible_decryptions = select_decryptions_matching_reliable_chars(encrypted_phrase, possible_decryptions)

    partial_decryption_tree = PartialDecryptionTree(encrypted_phrase, possible_decryptions)

    try:
        partial_decryption_tree.create_best_decryptions()
    except KeyboardInterrupt:
        partial_decryption_tree.print_best_decryptions(after_interruption=True)
        # partial_decryption_tree.print_best_decryptions(with_encoding_decoding_strings=True,
        #                                                after_interruption=True)
    else:
        partial_decryption_tree.print_best_decryptions()
        partial_decryption_tree.print_best_decryptions(with_encoding_decoding_strings=True)

    # print_possible_decryptions(encrypted_phrase, possible_decryptions)


# t0 = time.time()
# _i = 0
# for dict1 in (decryption[1] for decryption in possible_decryptions["RMJ"]):
#     for dict2 in (decryption[1] for decryption in possible_decryptions["IRF"]):
#         if matching_dictionaries(dict1, dict2):
#             dict2.update(dict1)
#             dict2[" "] = " "
#             print("".join([dict2.get(char, "?") for char in "RMJ IRF"]), dict2)
#             _i += 1
# print(_i)
# print(time.time() - t0)