# Readability Score

Project page: https://hyperskill.org/projects/155

## Example

```
$ rs.py --infile in.txt --words words.txt
The text is:
Readability is the ease with which a reader can understand a written text.
In natural language, the readability of text depends on its content and its presentation.
Researchers have used various factors to measure readability.
Readability is more than simply legibility, which is a measure of how easily a reader can distinguish individual letters or characters from each other.
Higher readability eases reading effort and speed for any reader, but it is especially important for those who do not have high reading comprehension.
In readers with poor reading comprehension, raising the readability level of a text from mediocre to good can make the difference between success and failure.

Words: 108
Difficult words: 25
Sentences: 6
Characters: 581
Syllables: 196
Polysyllables: 23
Enter the score you want to calculate (ARI, FK, SMOG, CL, DC, all): all

Automated Readability Index: 13 (about 24 year olds)
Flesch–Kincaid readability tests: 13 (about 24 year olds)
Simple Measure of Gobbledygook: 14 (about 24 year olds)
Coleman–Liau index: 14 (about 24 year olds)
Dale-Chall score: 8.18 (about 18 year olds)

This text should be understood in average by 22.8 year olds.
```
