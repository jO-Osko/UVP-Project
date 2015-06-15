import json
import os.path

__author__ = 'Filip'


class Trie():
    ENDING = "00"

    def __init__(self, trie=None, end=ENDING):
        if trie is None:
            trie = dict()
        self.root = trie
        self.end = end

    def add_word(self, word, uid):
        current_root = self.root
        for letter in word:
            current_root = current_root.setdefault(letter, {})
        current_root.setdefault(self.end, uid)

    def add_words(self, words, uids):
        for word, uid in zip(words, uids):
            current_root = self.root
            for letter in word:
                current_root = current_root.setdefault(letter, {})
            current_root.setdefault(self.end, uid)

    def add_word_dict(self, word_dict):
        for word in word_dict:
            current_root = self.root
            for letter in word:
                current_root = current_root.setdefault(letter, {})
            current_root.setdefault(self.end, word_dict[word])

    def add_word_pairs(self, word_pairs):
        for word, uid in word_pairs:
            current_root = self.root
            for letter in word:
                current_root = current_root.setdefault(letter, {})
            current_root.setdefault(self.end, uid)

    def remove_word(self, word):
        if word[0] in self.root:
            if len(word) > 1:
                root = Trie(self.root[word[0]])
                root.remove_word(word[1:])
            else:
                del self.root[word][self.end] # Nothing ends here now
            if len(self.root[word[0]]) == 0:
                del self.root[word[0]]
    
    def list_words_with_prefix(self, prefix):
        current_root = self.root
        for letter in prefix:
            if letter not in current_root:  # Nothing with this prefix
                return dict()
            current_root = current_root[letter]
        return self._list_all_words(prefix, current_root)


    def _list_all_words(self, prefix, parent):
        if parent == Trie.ENDING:
            return dict()
        results = dict()
        if Trie.ENDING in parent:
            results[prefix] = parent[Trie.ENDING]
        for key in parent.keys() - {Trie.ENDING}:
            results.update(self._list_all_words(prefix + key, parent[key]))
        return results

    def to_JSON(self, file_name=None):
        dump = json.dumps(self.root)
        if file_name is not None:
            open(file_name, "w").write(dump)
        return dump

    @classmethod
    def from_JSON_file(cls, file_name):
        if os.path.exists(file_name):
            return cls(trie=json.load(open(file_name, "r")))
        return cls()

    def __contains__(self, word):
        current_root = self.root
        for letter in word:
            current_root = current_root.get(letter)
            if not current_root:
                return False
        return Trie.ENDING in current_root



