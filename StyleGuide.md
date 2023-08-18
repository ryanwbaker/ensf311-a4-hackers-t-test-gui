# Style guide
## Author
The first line of all scripts (.py files), and the first cell of all notebooks (.ipynb files) need to contain your first and last name, e.g. `# Author: Yves Pauchard`

## Variable, function and method naming
Use lower case for variable, function and method names. Underscore to separate composed words, e.g. `all_names = ['alice', 'bob']`

## Class naming
Start class names with a capital letter and use camel-case for composed words, e.g. `class GraduateStudent()`

## Comments
Focus on _why_ not _what_ comments, use `#` to start a comment

## Docstring
For each function/method, include a docstring with the following format:
```python
"""one line description, what does the function do?

name (type): description

returns: (type) description
"""
```

An example:
```python
def remove_middle(text):
    """Removes middle character of odd length text, a copy otherwise.

    text (str): any string

    return: (str) even length string
    """
```

Additionally, for classes provide a description and list of attributes:
```python
class Point:
    """Represents a point in 2-D space.

    attributes: x, y
    """
```
