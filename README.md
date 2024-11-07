# boxed – a solver for New York Times Letter Boxed puzzle.

## Usage

The boxed.py script takes all the letters A-Z (or a-z) of its arguments and if
there are twelve letters, without any repeated letters, it splits them into four
groups of three to make a Letter Boxed puzzle, which it then tries to solve:

```console
$ ./boxed.py tiaUWLybdOMR
564 candidate words
LIMBO OUTWARDLY
```

Apart from the grouping by threes, the order of letters doesn't matter.

## Word lists and dictionaries

The boxed.py script works with any word list or dictionary file that lists
words one per line, and does not capitalize all words (as word lists often do).
Words with uppercase letters are ignored, as those are typically proper nouns
in a dictionary file.

By default, it looks for `box_dict.txt` in the current directory, and if that
doesn't exist, it uses `/usr/share/dict/words`. Set the environment variable
BOX_DICT to select an alternate word list file.

## Related work

There are other good resources for solving this type of puzzle:

- Alice Liang's [letter-boxed-solver (GitHub)][] and
  [live site](http://letterboxed.aliceyliang.com) is a very nice Flask app.
  The solving engine Alice created appears to be used in the following site.
- The [French `dcode` site] has added dictionary choices in several European
  languages.
- [Letter Boxed Answers] has user-contributed solutions, which provides more
  diversity of answers. It has historical puzzles and solutions going back to
  [21 July 2024](https://nytletterboxed.com/letter-boxed-july-21-2024-answers/).

[French `dcode` site]:
https://www.dcode.fr/letter-boxed-solver

[Letter Boxed Answers]:
https://nytletterboxed.com

[letter-boxed-solver (GitHub)]:
https://github.com/aliceyliang/letter-boxed-solver

## Credits

The `TWL06.txt` word list is a Scrabble tournament word list, it's taken
from the unmaintained [Anagram Thief](http://dcliu.com/projects/anagram-thief/)
[GitHub](https://github.com/iceboundflame/anagramthief) project. It's the
earliest GitHub instance of this file that I was able to find.
