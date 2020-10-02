#!/usr/bin/env python

import unittest

from math_trees.math_trees import MathTree

class TestMathTrees(unittest.TestCase):
    def test_basic_string(self):
        math_string = "3.4 + 4 * 2.8"
        mt = MathTree()
        mt.buildMathTree(math_string)
        value = mt.evaluate()
        self.assertEqual(value, eval(math_string))

    def test_another_string(self):
        math_string = "8 - 9.6 / 3"
        mt = MathTree()
        mt.buildMathTree(math_string)
        value = mt.evaluate()
        self.assertEqual(value, eval(math_string))

    def test_paren_string(self):
        math_string = "(-8.4 - 9 / 3.7) * 5.008 + (8.2 - 5.5)/8"
        mt = MathTree()
        mt.buildMathTree(math_string)
        value = mt.evaluate()
        self.assertEqual(value, eval(math_string))
