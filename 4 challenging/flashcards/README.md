# Flashcards

Project page: https://hyperskill.org/projects/127

## Examples

```
$ python flashcards.py
Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
add
The card:
France
The definition of the card:
Paris
The pair ("France":"Paris") has been added.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
add
The card:
Germany
The definition of the card:
Berlin
The pair ("Germany":"Berlin") has been added.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
add
The card:
Japan
The definition of the card:
Tokyo
The pair ("Japan":"Tokyo") has been added.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
log
File name:
log.txt
The log has been saved.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
export
File name:
capitals.txt
3 cards have been saved.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
exit
Bye bye!
```

```
$ python flashcards.py --import_from=capitals.txt --export_to=capitals.txt
3 cards have been loaded.
Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
ask
How many times to ask?
4
Print the definition of "Japan":
anime 
Wrong. The right answer is "Tokyo".
Print the definition of "Germany":
Berlin
Correct!
Print the definition of "Japan":
Tokyo
Correct!
Print the definition of "Japan":
what, again?
Wrong. The right answer is "Tokyo".

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
hardest card
The hardest card is "Japan". You have 2 errors answering it.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
reset stats
Card statistics have been reset.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
hardest card
There are no cards with errors.

Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):
exit
Bye bye!
3 cards have been saved.
```
