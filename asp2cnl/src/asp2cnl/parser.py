import lark
from lark import Transformer, Discard
from dataclasses import dataclass

from io import StringIO


class ASPTransformer(Transformer):
    __rules_list = []
        
    __lastConjunction = None
    __lastBodyLiterals = []    
    __thereIsNaf = False

    def start(self, elem):
        return ASPContentTree(self.__rules_list)
    
    def head(self, elem):   
        disElements = []
        for e in elem[0]:            
            if type(e) == ClassicalLiteral:
                disElements.append(e)            
        return Disjunction(disElements)

    def disjunction(self, elem):                    
        disElements = []
        for e in elem:            
            if type(e) == ClassicalLiteral:
                disElements.append(e)            
            else:              
                for e1 in e:
                    if type(e1) == ClassicalLiteral:  
                        disElements.append(e1)                              
        return disElements


    def classical_literal(self, elem):                            
        classicalLit = ClassicalLiteral(elem[0].value, elem[2][:])                                     
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

    def terms(self, elem):             
        terms = []
        for t in elem:
            if type(t) == Term:
                terms.append(t)
            else:              
                for t1 in t:
                    if type(t1) == Term:  
                        terms.append(t1)        
        return terms
                
    def term(self, elem):         
        return Term(elem[0].value)        

    def body(self, elem):  
       self.__lastConjunction = Conjunction(self.__lastBodyLiterals[:])             

        
    def statement(self, elem):         
        head = None
        for e in elem: 
            if type(e) == Disjunction:
                head = e     
        self.__rules_list.append(Rule(head, self.__lastConjunction))        
        self.__lastBodyLiterals = []
        return elem            

@dataclass(frozen=True)
class Term:
    name: str
    def isVariable(self):
        return not self.name.isnumeric() and self.name[0].isupper()
    def isUnderscore(self):
        return self.name == "_"
    def toString(self):
        return self.name

@dataclass(frozen=True)
class BuiltinAtom:
    op: str
    terms: list[Term]
    def toString(self):
        return self.terms[0].toString() + " " + self.op + " " + self.terms[1].toString()

@dataclass(frozen=True)
class ClassicalLiteral:
    name: str
    terms: list[Term]
    def toString(self):
        text = StringIO()   
        text.write(self.name)
        started = False
        for t in self.terms:
            if started:
                text.write(", ")
            else:
                text.write("(")
                started = True
            text.write(t.toString())
        if started:
            text.write(")")
        return text.getvalue()

@dataclass(frozen=True)
class NafLiteral:
    isNot: bool
    literal: ClassicalLiteral | BuiltinAtom 
    def toString(self):
        text = ""
        if self.isNot:
            text = "not "
        text = text + self.literal.toString()
        return text
    

@dataclass(frozen=True)
class Conjunction:
    literals: list[NafLiteral] 
    def hasVariables(self):
        for lit in self.literals:
            for term in lit.classical_literal.terms:
                if term.isVariable():
                    return True
        return False
    def toString(self):
        text = StringIO()           
        started = False
        for l in self.literals:
            if started:
                text.write(", ")
            else:                
                started = True
            text.write(l.toString())        
        text.write(".")
        return text.getvalue()

@dataclass(frozen=True)
class Choice:
    lowerGuard: Term  
    upperGuard: Term
    lowerOp: str
    upperOp: str
    literal: NafLiteral
    

@dataclass(frozen=True)
class Disjunction:
    atoms: list[ClassicalLiteral] 
    def hasVariables(self):
        for atom in self.atoms:
            for term in atom.terms:
                if term.isVariable():
                    return True
        return False
    def toString(self):
        text = StringIO()           
        started = False
        for a in self.atoms:
            if started:
                text.write(" | ")
            else:                
                started = True
            text.write(a.toString())                
        return text.getvalue()

@dataclass(frozen=True)
class Rule:
    head: Disjunction
    body: Conjunction
    def isFact(self):
        return self.head is not None and len(self.head.atoms) == 1 and self.body is None and not self.head.atoms[0].hasVariables()
    def isClassical(self):
        return self.head is not None and len(self.head.atoms) == 1 and self.body is not None and len(self.body.literals) > 0
    def isStrongConstraint(self):
        return self.head is None and self.body is not None and len(self.body.literals) > 0
    def isDisjunctive(self):
        return self.head is not None and len(self.head.atoms) > 1 and self.body is not None and len(self.body.literals) > 0

    def toString(self):
        text = StringIO() 
        if self.head is not None:
            text.write(self.head.toString())
        if self.body is None:
            text.write(".")
        else:
            text.write(" :- ")
            text.write(self.body.toString())
        return text.getvalue()
            
  
@dataclass(frozen=True)
class ASPContentTree:
    rules: list
