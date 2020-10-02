# Evaluating math expressions

Make math expressions with trees


## Getting Started
```
    git clone https://github.com/spboyle/math-trees`
    cd math-trees
    pip install -r requirements_dev.txt
    python setup.py develop
```

### Running tests
`python setup.py test`


## Code Challenge
Please code the following. Feel free to add to or re-structure the project as needed.
1. Create a data structure which can represent math expressions that supports the following:
  * Real numbers
  * plus(+)
  * minus(-)
  * times(*)
  * divide(/)
2. Implement an evaluation method which calculates the value of the expression
3. Write a parser which can convert a string containing a valid composition of any of the above operations to your data structure
4. Implement a `__str__` method which converts a math tree into an ascii string equivalent
5. Enhance the string parser you wrote in step #3 to handle parentheses ()


We would expect this work to take about four hours, but take however much time you'd like on this. Complete as much as you are able, but don't feel that you have to complete every item. They are ordered by difficultly, so we suggest coding to each requirement in number order.


## Credits
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
