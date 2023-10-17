import lark
from lark import Transformer, Discard
from dataclasses import dataclass


class ASPTransformer(Transformer):
    __rules_list = []

    __last_disjunction_list = []
    __last_termsList = []
    __open_parenthetis = False 

    __thereIsBody = False
    __thereIsOR = False

    def start(self, elem):
        return ASPContentTree(self.__rules_list)
    
    def head(self, elem):
        #print(elem)
        return elem


    def disjunction(self, elem):             
        self.__last_disjunction_list.append(Disjunction(elem))        

    def classical_literal(self, elem):  
        if (self.__open_parenthetis):
            self.__last_termsList.append(elem[0].value)
            self.__last_disjunction_list = []      
        else:
            classicalLit = ClassicalLiteral(elem[0].value, self.__last_termsList[:])             
            self.__last_termsList = []
            return classicalLit

         

    def term(self, elem):         
        self.__last_termsList.append(elem[0].value)
        self.__last_disjunction_list = []

    def body(self, elem):                    
        self.__thereIsBody = True

    def OR(self, elem):                    
        self.__thereIsOR = True
        
    def statement(self, elem):
        if not self.__thereIsBody:         
            self.__rules_list.append(Rule(self.__last_disjunction_list[:]))        
            self.__last_disjunction_list = []        
        self.__thereIsBody = False
        return elem

    def PAREN_OPEN(self, elem): 
        self.__open_parenthetis = True   
    
    def PAREN_CLOSE(self, elem): 
        self.__open_parenthetis = False
        

@dataclass(frozen=True)
class ClassicalLiteral:
    name: str
    terms: list[str]



@dataclass(frozen=True)
class Disjunction:
    atoms: list[ClassicalLiteral] 
    def hasVariables(self):
        for atom in self.atoms:
            for term in atom.terms:
                if not term.isnumeric() and term[0].isupper():
                    return True
        return False

@dataclass(frozen=True)
class Rule:
    head: list[Disjunction]
    body = []   # TODO
    def isFact(self):
        return len(self.head) == 1 and len(self.body) == 0 and not self.head[0].hasVariables()
  
@dataclass(frozen=True)
class ASPContentTree:
    rules: list
