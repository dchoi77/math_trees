"""Main module."""

from pythonds.trees import BinaryTree
from collections import defaultdict
import re
   
class MathTree():
    def __init__(self):
        # Precedence of operators
        self.pred = defaultdict(lambda: 10)
        self.pred['('] = 1
        self.pred[')'] = 1
        self.pred['+'] = 2
        self.pred['-'] = 2
        self.pred['*'] = 3
        self.pred['/'] = 3

        # A node contains a string value that represents
        # either an operator or a number.
        # A node also can contain other information, if necessary.
        # For example, if we run add_nterms(), then 
        # each node contains the number of terms at the subtree rooted at the node.
        # The default root contains '(' as its value.
        self.mTree = BinaryTree({'val':'(',})

    def __str__(self):
        # Compute the number of terms at each node.
        self.add_nterms(self.mTree)
        return self.__str(self.mTree)
    
    def __str(self, cRoot):
        data = cRoot.getRootVal()
        
        if data['val'] in list('+-*/'):
            l = self.__str(cRoot.leftChild)
            r = self.__str(cRoot.rightChild)

            # left_expr + right_expr            
            if data['val'] == '+':
                return l + ' + ' + r
            # left_expr - right_expr, if right_expr consists of one term.
            # left_expr - ( right_expr ), otherwise.
            elif data['val'] == '-':
                return l + ' - ' + (r if cRoot.rightChild.getRootVal()['ntm'] == 1 else '( ' + r + ' )')
            # left_expr * right_expr, if both left_expr and right_expr consist of one term.
            # If an expression consists of multiple terms, we need to use '(' and ')' around it. 
            elif data['val'] == '*':
                return (l if cRoot.leftChild.getRootVal()['ntm'] == 1 else '( ' + l + ' )') \
                    + ' ' + data['val'] + ' ' \
                    + (r if cRoot.rightChild.getRootVal()['ntm'] == 1 else '( ' + r + ' )')
            # left_expr / right_expr, if left_expr consists of one term and right_expr consists of a number
            # If left_expr has multiple terms, use '( left_expr )'.
            # If right_expr is a not a number, use '( right_expr )'.
            else:
                try:
                    _ = float(r)
                except:
                    r = '( ' + r + ' )'
                        
                return (l if cRoot.leftChild.getRootVal()['ntm'] == 1 else '( ' + l + ' )') \
                    + ' ' + data['val'] + ' '  + r
        # if data['val'] is a number, return it.
        else:
            return data['val']


    # Example: 2 + 3 has two terms. 
    # In that case, left_child node has {'val':'2', 'ntm': 1},
    # right_child node has {'val':'3', 'ntm': 1},
    # and the root node has {'val': '+', 'ntm': 2}
    # Knowing the number of terms at each subtree is useful in __str__().
    def add_nterms(self, cRoot):
        data = cRoot.getRootVal()

        # If op is either '+' or '-', then
        # num_terms_in_root = num_terms_in_left_expr + num_terms_in_right_expr
        if data['val'] in list('+-'):
            self.add_nterms(cRoot.leftChild)
            self.add_nterms(cRoot.rightChild)
            data['ntm'] = cRoot.leftChild.getRootVal()['ntm']\
                + cRoot.rightChild.getRootVal()['ntm']
        # If op is '*' or '/', then
        # num_terms_in_root = 1
        elif data['val'] in list('*/'):
            data['ntm'] = 1
            self.add_nterms(cRoot.leftChild)
            self.add_nterms(cRoot.rightChild)
        # If we have a number, then num_terms is 1.
        else:
            data['ntm'] = 1
           
        
    def buildMathTree(self, expr):
        tokens = self.parseExpr(expr)
        pRoots= []             # list of parent roots
        cRoot = self.mTree     # current root
        
        for c in tokens:
            if c == '(':
                cRoot.insertRight({'val':'(',})
                pRoots.append(cRoot)
                cRoot = cRoot.getRightChild()
            elif c == ')':
                while(pRoots[-1].getRootVal()['val'] != '('):
                    pRoots.pop()
                openParen = pRoots.pop()
                cRoot = pRoots.pop()
                cRoot.rightChild = openParen.rightChild
            else:
                curr_pred = self.pred[cRoot.getRootVal()['val']]
                new_pred = self.pred[c]
                
                while(curr_pred >= new_pred):
                    cRoot = pRoots.pop()
                    curr_pred = self.pred[cRoot.getRootVal()['val']]
                    
                newNode = BinaryTree({'val':c,})
                newNode.leftChild = cRoot.rightChild
                cRoot.rightChild = newNode
                pRoots.append(cRoot)
                cRoot = newNode
                
        self.mTree = pRoots[0].rightChild if len(pRoots)>0 else cRoot.rightChild 
        return self.mTree
                                        
    def parseExpr(self, expr):
        tokens = re.findall(r"\d+(?:\.\d+)?|[\*/\(\)+-]", expr)
        # '+' or '-' is a sign, if
        # '(', '+|-', number
        # '+|-', number
        for i in range(len(tokens)):
            if tokens[i] == '(' and tokens[i+1] in list('+-'):
                if tokens[i+1] == '-':
                    tokens[i+2] = '-' + tokens[i+2];
                tokens[i+1] = ''
  
        if tokens[0] in list('+-'):
            if tokens[0] == '-': 
                tokens[1] = '-' + tokens[1]
            tokens[0] = ''
            
        return [c for c in tokens if len(c)>0]
    
    def evaluate(self):
        return self.__eval(self.mTree)
    
    def __eval(self, cRoot):
        c = cRoot.getRootVal()['val'] 
        if c in list('+-*/'):
            l = self.__eval(cRoot.leftChild)
            r = self.__eval(cRoot.rightChild)
            return eval(str(l) + c + str(r))
        else:
            return float(c)

# Simple Test
# mt = MathTree()
# expr = '((2.1 - 3) + 5) / 4.2 - (3.8 + 7)'
# print('original_expr:', expr)
# mt.buildMathTree(expr)
# print('tree_expr:', mt)
# print('original_eval:', eval(expr))
# print('tree_eval:', mt.evaluate())