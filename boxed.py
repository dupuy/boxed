#!/usr/bin/env python3
"""boxed – a solver for New York Times Letter Boxed puzzle."""
import os
import re
import string
import sys

from collections import defaultdict

sorted_wordmap: dict[str, list[tuple]] = {}

letters = re.sub("[^a-z]", "", "".join(sys.argv[1:]).lower())
letter_set = {letter for letter in letters}
complete = len(letters)
if len(letter_set) != complete:
    print(f"Duplicate letter in '{letters.upper()}'", file=sys.stderr)
    exit(1)
if complete != 12:
    quantity = "few" if complete < 12 else "more"
    print(f"Too {quantity} letters in '{letters.upper()}'", file=sys.stderr)
    exit(1)
sides = re.fullmatch("(...)(...)(...)(...)", letters)
groups = [sides[1], sides[2], sides[3], sides[4]]
validity = [re.compile(f"[^{letters}]")] + [
    re.compile(f"[{groups[i]}][{groups[i]}]") for i in range(4)
]


def ranking(word: str) -> int:
    """Return number of distinct letters in word."""
    return len({letter for letter in word})


solutions_by_word1: dict[str, str] = {}
solutions_by_word2: dict[str, str] = {}


def insert_solution(solution_dict: dict[str, str], key: str, value: str):
    # up_key = key.upper()
    # up_val = value.upper()
    other = solution_dict.get(key, "xx")
    if other and value.startswith(other):
        # print(f"\t\t\t keep {other.upper()}, ignore {up_val} for {up_key}")
        return
    # elif other and other.startswith(value):
    #     print(f"\t\t\t replace {other.upper()} with {up_val} for {up_key}")
    solution_dict[key] = value


def evaluate(word1: str, rank1: int, word2: str, rank2: int) -> None:
    if rank1 + rank2 <= complete:  # at least one letter is common to the two
        return
    combined = ranking(word1 + word2)
    # if combined > 9:
    #     print(f"{word1}({rank1}) + {word2}({rank2}) = {combined}")
    if combined != complete:
        return

    insert_solution(solutions_by_word1, word1, word2)
    insert_solution(solutions_by_word2, word2, word1)


def getwords(word_file: str) -> dict[str, set[tuple[int, str]]]:
    """Load ranked valid words into word map."""

    word_map: dict[str, set[tuple[int, str]]] = {
        letter: set() for letter in string.ascii_lowercase
    }

    with open(word_file) as words:
        wordcount = 0
        plurals_added = 0
        pluralizable = ""
        # Traditional dictionaries don't include plurals, but game word lists do.
        if "s" in letters and "/dict/" in word_file:
            pluralizable = letters.replace(groups[letters.index('s') // 3], "")

        for candidate in words:
            candidate = candidate.strip()
            for check in validity:
                if (not 2 < len(candidate) < 16) or re.search(check, candidate):
                    break
            else:
                word_rank = ranking(candidate)
                if word_rank == complete:
                    print(f"{candidate.upper()} is a soliton!")
                if word_rank > 2:
                    word_map[candidate[0]].add((word_rank, candidate))
                    wordcount += 1
                    if candidate[-1] in pluralizable:
                        if "s" not in candidate:
                            word_rank += 1
                        candidate += "s"
                        word_map[candidate[0]].add((word_rank, candidate))
                        plurals_added += 1
                assert 1 < word_rank <= complete
        print(f"{wordcount} candidate words")
        if plurals_added:
            print(f"{plurals_added} added plurals")
    
    if wordcount == 0:
        print(f"No valid (lowercase) words in {word_file}", file=sys.stderr)
        exit(2)
    return word_map


word_list = "box_dict.txt"
word_list = os.getenv("BOX_DICT", word_list)

for file in [word_list, "/usr/share/dict/words"]:
    try:
        wordmap = getwords(file)
        break
    except OSError as os_err:
        seps = [os.pathsep, "/"]
        cwd = ""
        if not os_err.filename[0] in seps:
            cwd = f" in '{os.getcwd()}'"
        print(f"{os_err.strerror}: '{os_err.filename}'{cwd}", file=sys.stderr)
else:
    exit(2)

for letter in wordmap.keys():
    sorted_wordmap[letter] = sorted(wordmap[letter], reverse=True)

finals = {
    last for last in sorted_wordmap.keys() if len(sorted_wordmap[last]) > 0
}
if sorted(finals) != sorted(letters):
    missing = [letter for letter in letters if letter not in finals]
    print(f"These non-starter letters start no words: {sorted(missing)}")

ignored = 0
for start in sorted_wordmap.keys():
    if len(sorted_wordmap[start]) == 0:
        continue
    for rank, first in sorted_wordmap[start]:
        following = first[-1]
        if following not in finals:
            ignored += 1
            continue
        for next_rank, second in sorted_wordmap[following]:
            evaluate(first, rank, second, next_rank)

if ignored > 0:
    print(f"Ignored {ignored} first words ending with a non-starter")

solutions_set: dict[str, int] = {}
for first, second in solutions_by_word1.items():
    solutions_set[f"{first.upper()} {second.upper()}"] = len(first + second)

for second, first in solutions_by_word2.items():
    solutions_set[f"{first.upper()} {second.upper()}"] = len(first + second)

solutions_by_length: defaultdict[int, list[str]] = defaultdict(list)

for solution in solutions_set.keys():
    length = solutions_set[solution]
    solutions_by_length[length].append(solution)

sorted_lengths = sorted(solutions_by_length.keys())
limit = 0
solutions = 0
while solutions < 10 and limit < len(sorted_lengths):
    solutions += len(solutions_by_length[sorted_lengths[limit]])
    limit += 1
if solutions == 0:
    print("No solutions found!", file=sys.stderr)
    exit(3)
for length in sorted(solutions_by_length.keys())[0:limit]:
    print("\n".join(sorted(solutions_by_length[length])))
