from typing import Dict, List

from copy import deepcopy, copy

from dictionary_filter import dictionaries_match
from reliable_char_mapping import reliable_mapping


class PartialDecryptionNode:
    def __init__(self, partial_mapping):
        self.partial_decryption = partial_mapping
        self.children: List[PartialDecryptionNode] = []
        self.complete = False
        self.contradictory = False

    def __str__(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        decoding = "".join([self.partial_decryption.get(char, "?") for char in alphabet])
        return alphabet + "\n" + decoding

    def set_complete(self):
        self.complete = True

    def set_contradictory(self):
        self.contradictory = True

    def create_children(self, children_decryption_dict, max_dict_length):
        if self.contradictory:
            return
        for children_decryption in children_decryption_dict:
            children_decryption_dict = deepcopy(children_decryption)
            children_decryption_dict.update(self.partial_decryption)
            child = PartialDecryptionNode(children_decryption_dict)
            if not dictionaries_match(children_decryption, self.partial_decryption):
                child.set_contradictory()
                continue
            elif len(children_decryption_dict) >= max_dict_length:
                child.set_complete()
            self.children.append(child)

    def decrypt(self, word):
        decryption = copy(self.partial_decryption)
        decryption[" "] = " "
        decrypted = "".join(decryption.get(char, "?") for char in word)
        return decrypted

    def decoding_string(self):
        return str(self)

    def encoding_string(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
        reverse_dict = {v: k for k, v in self.partial_decryption.items()}
        encoding = "".join([reverse_dict.get(char, "?") for char in alphabet])
        return alphabet + "\n" + encoding

    def one_to_one(self):
        return len(set(self.partial_decryption.keys())) == len(set(self.partial_decryption.values()))


class PartialDecryptionTree:
    def __init__(self, encrypted_phrase, possible_decryptions):
        self.encrypted_phrase = encrypted_phrase
        self.encrypted_phrase_chars_count = len(set(encrypted_phrase))
        if " " in encrypted_phrase:
            self.encrypted_phrase_chars_count -= 1
        self.initial_possible_decryptions = possible_decryptions
        self.max_depth = len(possible_decryptions) - 1
        self.nodes_levels : Dict[int, List[PartialDecryptionNode]]= {}
        self.sorted_initial_decryptions = sorted(possible_decryptions.values(),
                                                 key=lambda decryption: (len(decryption), -len(decryption[0])))
        initial_reliable_mapping = reliable_mapping(self.sorted_initial_decryptions[0])
        self.root = PartialDecryptionNode(initial_reliable_mapping)
        self.nodes_levels[-1] = [self.root]
        self.complete_decryptions = []

    def current_level(self):
        return len(self.nodes_levels) - 2

    def create_next_level_children(self):
        level = self.current_level()
        next_level = level + 1
        self.nodes_levels[next_level] = []
        for node in self.nodes_levels[level]:
            node.create_children(self.sorted_initial_decryptions[next_level], self.encrypted_phrase_chars_count)
            self.nodes_levels[next_level] += node.children

    def create_best_decryptions(self):
        for level in range(self.max_depth + 1):
            self.print_progress()
            if not all(node.contradictory for node in self.nodes_levels[level-1]):
                self.create_next_level_children()
            else:
                break

    def check_all_complete(self, nodes):
        return all(node.complete for node in nodes)

    def check_all_one_to_one(self, nodes):
        return all(node.one_to_one() for node in nodes)

    def select_best_decryptions(self, only_one_to_one_if_possible, only_complete_if_possible, after_interruption):
        best_level = -1
        max_level = self.current_level()
        if after_interruption:
            max_level -= 1
        for level in range(max_level, -2, -1):
            if not all(node.contradictory for node in self.nodes_levels[level]):
                best_level = level
                break
        best_nodes = [node for node in self.nodes_levels[best_level] if not node.contradictory]
        if only_complete_if_possible and any(node.complete for node in best_nodes):
            best_nodes = [node for node in best_nodes if node.complete]
        if only_one_to_one_if_possible and any(node.one_to_one() for node in best_nodes):
            best_nodes = [node for node in best_nodes if node.one_to_one()]
        return best_nodes

    def print_decryptions(self, decryptions_nodes: List[PartialDecryptionNode], *,
                          with_encoding_decoding_strings=False,
                          after_interruption=False):
        print()
        all_complete = self.check_all_complete(decryptions_nodes)
        all_one_to_one = self.check_all_one_to_one(decryptions_nodes)
        if after_interruption:
            print("Deszyfrowanie przerwane, wyświetlam najlepsze znalezione dotchczas wyniki")
            print(f"Liczba możliwych deszyfrowań: {len(decryptions_nodes)}")
        if all_complete:
            print("Wszystkie odwzorowania kompletne")
        if all_one_to_one:
            print("Wszystkie odwzorowania 1-1")
        print()
        for node in decryptions_nodes:
            print(node.decrypt(self.encrypted_phrase))
            if not all_one_to_one and node.one_to_one():
                print("Odzworowanie 1-1 -- można szyfrować i deszyfrować")
            if not all_complete and node.complete:
                print("Odwzorowanie kompletne -- każda litera tekstu ma swój odpowiednik")
            if with_encoding_decoding_strings:
                print("Wzór deszyfrowania:", node.decoding_string(), sep="\n")
                print("Wzór szyfrowania:", node.encoding_string(), sep="\n")
            print()
        print(f"Znaleziono {len(decryptions_nodes)} możliwych rozwiązań")

    def print_best_decryptions(self, *,
                               with_encoding_decoding_strings=False,
                               only_one_to_one_if_possible=True,
                               only_complete_if_possible=True,
                               after_interruption=False):
        best_decryptions = self.select_best_decryptions(only_one_to_one_if_possible,
                                                        only_complete_if_possible,
                                                        after_interruption)
        self.print_decryptions(best_decryptions,
                               with_encoding_decoding_strings=with_encoding_decoding_strings,
                               after_interruption=after_interruption)

    def print_progress(self):
        print(f"Głębokość w drzewie: {self.current_level()+1} z {self.max_depth}")
        print(f"Liczba rozpatrywanych przypadków: {len(self.nodes_levels[self.current_level()])}")


