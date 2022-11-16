# Welcome to Renloi
Renloi is a general-purpose blazingly-fast compiled programming language with minimal runtime.
## Requirements
If you want to run Renloi from the source, you should have python 3.10 or greater installed.

A recent version of gcc/g++, with the c++ boost library version 1.7.9.
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
```py
number = 10
word = "Ten"
print(name)
print(word)
```
## Writing data to files
```py
content = "Wow, This is a text file!"
write("textfile.txt", content)
```
## Reading data from files
```py
content = read("textfile.txt")
print(content)
```
## Generating a random number
```py
import random
number = random.randint(1, 10) # The generated number will be a number from 1 to 10.
print(number)
```
