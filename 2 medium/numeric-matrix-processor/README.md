# Numeric Matrix Processor

Project page: https://hyperskill.org/projects/96

## Examples

```
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
```

### 1. Addition

```
Your choice: 1
Enter size of first matrix: 1 2
Enter first matrix:
0.1 -2
Enter size of second matrix: 1 2
Enter second matrix:
333 -0.44
The result is:
333.1 -2.44
```

### 2. Multiplication by number

```
Your choice: 2
Enter matrix size: 3 2
Enter matrix:
1 2
3 4
5 6
Enter constant: 0.5
The result is:
0.5   1
1.5   2
2.5   3
```

### 3. Matrix by matrix multiplication

```
Your choice: 3
Enter size of first matrix: 2 2
Enter first matrix:
1 2
3 4
Enter size of second matrix: 3 3
Enter second matrix:
1 2 3
4 5 6
7 8 9
The operation cannot be performed.
```

```
Your choice: 3
Enter size of first matrix: 2 3
Enter first matrix:
0.1 0.2 0.3
-4 -5 -6
Enter size of second matrix: 3 2
Enter second matrix:
10 10
10 10
10 10
The result is:
   6    6
-150 -150
```

### 4. Transposition

```
Your choice: 4

1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
```

#### 4.1 Along the main diagonal

```
Your choice: 1
Enter matrix size: 4 4
Enter matrix:
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
The result is:
 1  5  9 13
 2  6 10 14
 3  7 11 15
 4  8 12 16
```

#### 4.2 Along the side diagonal

```
Your choice: 2
Enter matrix size: 4 4
Enter matrix:
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
The result is:
16 12  8  4
15 11  7  3
14 10  6  2
13  9  5  1
```

#### 4.3 Along the vertical line

```
Your choice: 3
Enter matrix size: 4 4
Enter matrix:
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
The result is:
 4  3  2  1
 8  7  6  5
12 11 10  9
16 15 14 13
```

#### 4.4 Along the horizontal line

```
Your choice: 4
Enter matrix size: 4 4
Enter matrix:
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
The result is:
13 14 15 16
 9 10 11 12
 5  6  7  8
 1  2  3  4
```

### 5. Determinant

```
Your choice: 5
Enter matrix size: 5 5
Enter matrix:
1 2 3 4 5
4 5 6 4 3
0 0 0 1 5
1 3 9 8 7
5 8 4 7 11
The result is:
191
```

### 6. Inversion

```
Your choice: 6
Enter matrix size: 3 3
Enter matrix:
1 2 3
4 5 6
7 8 9
This matrix doesn't have an inverse.
```

```
Your choice: 6
Enter matrix size: 3 3
Enter matrix:
2 -1 0
0 1 2
1 1 0
The result is:
 0.333      0  0.333
-0.333      0  0.667
 0.167    0.5 -0.333
```
