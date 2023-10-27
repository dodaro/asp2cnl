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
    __thereIsNaf = False

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

    def NAF(self, elem):
        self.__thereIsNaf = True        

    def naf_literal(self, elem):
        classical_lit = None
        if len(elem) == 1:
            classical_lit = elem[0]
        else:
            classical_lit = elem[1]
        nafLit = NafLiteral(self.__thereIsNaf, classical_lit)
        self.__lastBodyLiterals.append(nafLit) 
        self.__thereIsNaf = False        
        return elem

    def binop(self, elem):
        return elem[0]
    
    def EQUAL(self, elem):        
        return elem.value
    def GREATER(self, elem):
        return elem.value
    def GREATER_OR_EQ(self, elem):
        return elem.value
    def LOWER(self, elem):
        return elem.value
    def LOWER_OR_EQ(self, elem):
        return elem.value
    def UNEQUAL(self, elem):
        return elem.value        

    def builtin_atom(self, elem):          
        return BuiltinAtom(elem[0][1], [elem[0][0], elem[1]])  

    def b(self, elem):
        return elem

    def term(self, elem):         
        self.__last_termsList.append(Term(elem[0].value))
        return Term(elem[0].value)        

    def body(self, elem):  
       self.__lastConjunction = Conjunction(self.__lastBodyLiterals[:])             

    def OR(self, elem):                    
        self.__thereIsOR = True
        
    def statement(self, elem):        
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
class BuiltinAtom:
    op: str
    terms: list[Term]

@dataclass(frozen=True)
class ClassicalLiteral:
    name: str
    terms: list[Term]

@dataclass(frozen=True)
class NafLiteral:
    isNot: bool
    literal: ClassicalLiteral | BuiltinAtom 

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
