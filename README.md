# Renloi
A general-purpose blazingly fast compiled programming language with minimal runtime. Current version is 1.0.0.
## Requirements
If you want to run Renloi from the source, you should have python 3.10 or greater installed.

A recent version of gcc/g++.
# Code Reference
This is a simple guide about all the features included in Renloi. Let's start with a simple "Hello, World!" Program.
## Hello, World!
Without using a function

```py
print("Hello, World")
```
Using a function:

```py
def helloworld():
    print("Hello, World")

def main():
    helloworld() 
```


As you can see from the code example above, your program starts executing in the main() function.

Note: All the functions you want to include inside the main function, needs to be written above the main function.

If you didn't declare any function, you don't need to use the main() function.

## Declaring variables
number = 10
word = "Ten"
print(name)
print(word)
