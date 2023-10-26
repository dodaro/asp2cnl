import lark
from lark import Transformer, Discard
from dataclasses import dataclass


class ASPTransformer(Transformer):
    __rules_list = []

    __last_disjunction_list = []
    __last_termsList = []
    __open_parenthetis = False 

    __lastConjunction = None
    __lastBodyLiterals = []
    __thereIsOR = False

    def start(self, elem):
        return ASPContentTree(self.__rules_list)
    
    def head(self, elem):                
        return elem

    def disjunction(self, elem):                   
        self.__last_disjunction_list.append(Disjunction(elem))        

    def classical_literal(self, elem):  
        if (self.__open_parenthetis):
            self.__last_termsList.append(elem[0].value)
            #self.__last_disjunction_list = []      
        else:
            classicalLit = ClassicalLiteral(elem[0].value, self.__last_termsList[:])             
            self.__last_termsList = []
            return classicalLit
         
    def naf_literal(self, elem):
        self.__lastBodyLiterals.append(elem) 
        #nafLit = NafLiteral(elem)
        return elem

    def term(self, elem):         
        self.__last_termsList.append(Term(elem[0].value))
        #self.__last_disjunction_list = []

    def body(self, elem):  
       self.__lastConjunction = Conjunction(self.__lastBodyLiterals[:])             

    def OR(self, elem):                    
        self.__thereIsOR = True
        
    def statement(self, elem):
        #print("ST " + elem)  
        #print(self.__lastBody[:])
        self.__rules_list.append(Rule(self.__last_disjunction_list[:], self.__lastConjunction))
        self.__last_disjunction_list = []                
        self.__lastBodyLiterals = []
        return elem

    def PAREN_OPEN(self, elem): 
        self.__open_parenthetis = True   
    
    def PAREN_CLOSE(self, elem): 
        self.__open_parenthetis = False
        

@dataclass(frozen=True)
class Term:
    name: str
    def isVariable(self):
        return not self.name.isnumeric() and self.name[0].isupper()
    def isUnderscore(self):
        return self.name == "_"

@dataclass(frozen=True)
class ClassicalLiteral:
    name: str
    terms: list[Term]

@dataclass(frozen=True)
class NafLiteral:
    classical_literal: ClassicalLiteral    

@dataclass(frozen=True)
class Conjunction:
    literals: list[NafLiteral] 
    def hasVariables(self):
        for lit in self.literals:
            for term in lit.classical_literal.terms:
                if term.isVariable():
                    return True
        return False

@dataclass(frozen=True)
class Disjunction:
    atoms: list[ClassicalLiteral] 
    def hasVariables(self):
        for atom in self.atoms:
            for term in atom.terms:
                if term.isVariable():
                    return True
        return False

@dataclass(frozen=True)
class Rule:
    head: list[Disjunction]
    body: list[Conjunction] 
    def isFact(self):
        return len(self.head) == 1 and self.body is None and not self.head[0].hasVariables()
    def isClassical(self):
        return len(self.head) == 1 and self.body is not None and len(self.body.literals) > 0
  
@dataclass(frozen=True)
class ASPContentTree:
    rules: list
