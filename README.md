# B1u3 Calculator

Calculator for arighmetic operations.

And you can use variables and functions.

This calculator has only one object type Integer.

This can not define a function in another function. 

# Installation

```
% pip install B1u3Calulator
```

# How to use

Start repl(Read-Eval-Print Loop)

```
% b1u3calculator
```

Start with file

```
% b1u3calculator -f foobar.txt
```

Start parser repl

```
% b1u3calculator -p
```

Start lexer repl

```
% b1u3calculator -l
```

# Grammer

## variable

```
foobar = 3
foobar = 3 * 5
foobar = a + b / c * 4
```

## function

```
def sample_func(a, b, c) {
    return a+b+c
}
```

or

```
def sample_func(a, b, c) {
    a+b+c;
}
```
