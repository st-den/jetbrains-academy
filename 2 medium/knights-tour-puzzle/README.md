# Knight's Tour Puzzle

Project page: https://hyperskill.org/projects/141

Uses [Warnsdorff's rule](https://en.wikipedia.org/wiki/Knight%27s_tour#Warnsdorff's_rule) and backtracking.

## Examples

```
Enter your board dimensions: > 5 4
Enter knight's starting position: > 1 4
Do you want to try the puzzle? (y/n): > y
 ------------------
4|  X __ __ __ __ |
3| __ __  5 __ __ |
2| __  3 __ __ __ |
1| __ __ __ __ __ |
 ------------------
    1  2  3  4  5
....

Enter your next move: > 2 4
 ------------------
4|  *  X  *  *  * |
3|  *  *  *  *  * |
2|  *  *  *  *  * |
1|  *  *  *  *  * |
 ------------------
    1  2  3  4  5

What a great tour! Congratulations!
```

```
Enter your board's dimensions: > 6 6
Enter the knight's starting position: > 1 6
Do you want to try the puzzle? (y/n): > n

Here's the solution!
 ---------------------
6|  1 30 27 12 15 36 |
5| 28 11  2  5 26 13 |
4| 31  4 29 14 35 16 |
3| 10 21 18  3  6 25 |
2| 19 32 23  8 17 34 |
1| 22  9 20 33 24  7 |
 ---------------------
    1  2  3  4  5  6
```
