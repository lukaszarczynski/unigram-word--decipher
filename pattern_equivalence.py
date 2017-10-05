DEBUG = False


def same_letters_indices(word):
    """Finds pairs of incices in which letters in words are the same"""
    same_letters = []
    for idx, letter in enumerate(word):
        for another_idx, another_letter in enumerate(word):
            if letter == another_letter and idx < another_idx:
                same_letters.append((idx, another_idx))
    if DEBUG:
        print(same_letters)
    return same_letters


def remove_polish_characters(word):
    """Replaces polish characters in words with their latin counterparts"""
    polish_characters = dict(zip("ęóąśłżźćń", "eoaslzzcn"))
    word = [polish_characters.get(char, char) for char in word]
    return "".join(word)


def equal_words(word1, word2):
    """Checks if words are equal modulo polish characters"""
    word1 = word1.lower()
    word2 = word2.lower()
    return remove_polish_characters(word1) == remove_polish_characters(word2)


def same_letters_match(word, same_letters_indices):
    """Checks if letters at given indices are the same"""
    return all(equal_words(word[idx1], word[idx2]) for idx1, idx2 in same_letters_indices)


def different_letters_match(word, same_letters_indices):
    """Check if all pairs of letters except ones at given indices are different"""
    letters_match = True
    for idx1, letter1 in enumerate(word):
        for idx2, letter2 in enumerate(word):
            if idx1 < idx2 and (idx1, idx2) not in same_letters_indices and word[idx1] == word[idx2]:
                letters_match = False
    return letters_match


def pattern_equivalence(word1):
    """Checks if word2 can be created from word1 with single letters substitutions (pattern equivalence)"""
    same_letters_1 = same_letters_indices(word1)

    def first_word_pattern_equivalence(word2):
        """Checks if word2 can be created from word1 with single letters substitutions (pattern equivalence)"""
        if same_letters_match(word2, same_letters_1) and different_letters_match(word2, same_letters_1):
            return True
        return False

    return first_word_pattern_equivalence

if __name__ == "__main__":
    assert set(same_letters_indices("melmażelon")) == {(0, 3), (1, 6), (2, 7)}
    assert remove_polish_characters("zażółć gęślą jaźń") == "zazolc gesla jazn"
    assert equal_words("zazolc gesla jazn", "zażółć gęślą jaźń")
    assert same_letters_match("aaabcd", [(0, 1)]) and not different_letters_match("aaabcd", [(0, 1)])
    assert different_letters_match("abc", [(0, 1)]) and not same_letters_match("abc", [(0, 1)])
    pattern_equivalence_aaabcd = pattern_equivalence("aaabcd")
    assert (pattern_equivalence_aaabcd("xxxdfg") and
            not pattern_equivalence_aaabcd("xxxddd") and
            not pattern_equivalence_aaabcd("xdfghj"))