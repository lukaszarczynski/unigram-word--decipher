from decrypt import create_pattern_equivalents_for_words_in_phrase, decrypt_with_given_dictionary


def print_possible_decryptions(encrypted_phrase, possible_decryptions):
    for encrypted_word in encrypted_phrase:
        print([(decrypt_with_given_dictionary(encrypted_word, decryption_dict), decryption_dict)
               for decryption_dict in possible_decryptions[encrypted_word]])


if __name__ == "__main__":
    encrypted_phrase = input().rstrip()

    possible_decryptions = create_pattern_equivalents_for_words_in_phrase(encrypted_phrase,
                                                                          minimum_occurrences_of_word=10)

    print_possible_decryptions(encrypted_phrase, possible_decryptions)