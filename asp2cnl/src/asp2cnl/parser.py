import lark
from lark import Transformer, Discard
from dataclasses import dataclass

from io import StringIO


class ASPTransformer(Transformer):
    __rules_list = []
                
    def start(self, elem):        
        return ASPContentTree(self.__rules_list)
    
    def head(self, elem):
        if len(elem) == 1 and type(elem[0]) == Choice:            
            return elem[0]
        else:            
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
        return "_NOT_"       

    def naf_literal(self, elem):        
        thereIsNaf = False
        lit = None
        for e in elem:
            if e == "_NOT_":
                thereIsNaf = True
            elif type(e) == ClassicalLiteral or type(e) == BuiltinAtom:
                lit = e        
        nafLit = NafLiteral(thereIsNaf, lit)                
        return nafLit

    def binop(self, elem):
        return elem[0]
    
    def EQUAL(self, elem):        
        return elem.value
    def GREATER(self, elem):
        return elem.value
    def GREATER_OR_EQ(self, elem):
        return elem.value
    def LESS(self, elem):
        return elem.value
    def LESS_OR_EQ(self, elem):
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

    def COLON(self, elem):
        return "_COLON_"

    def CONS(self, elem):
        return "_IF_"

    def CURLY_OPEN(self, elem):
        return "_CURLY_OPEN_"
    def CURLY_CLOSE(self, elem):
        return "_CURLY_CLOSE_"
        
    def choice(self, elem):  
        lowerGuard = None
        upperGuard = None
        lowerOp = None
        upperOp = None
        choice_elements = None
        foundCurlyOpen = False
        foundCurlyClose = False
        for e in elem:
            if e == "_CURLY_OPEN_":
                foundCurlyOpen = True
            elif e == "_CURLY_CLOSE_":
                foundCurlyClose = True
            else:
                if type(e) == Term:
                    if not foundCurlyOpen:
                        lowerGuard = e
                    elif foundCurlyClose:
                        upperGuard = e
                elif type(e) == str:
                    if not foundCurlyOpen:
                        lowerOp = e
                    elif foundCurlyClose:
                        upperOp = e
                else:
                    choice_elements = e                    
        return Choice(lowerGuard, upperGuard, lowerOp, upperOp, choice_elements)
    

    def choice_elements(self, elem): 
        choiceElements = []
        for e in elem:            
            if type(e) == ChoiceElement:
                choiceElements.append(e)            
            else:              
                for e1 in e:
                    if type(e1) == ChoiceElement:  
                        choiceElements.append(e1)                              
        return choiceElements

    def choice_element(self, elem): 
        left_part = None
        right_part = None
        foundColon = False
        for e in elem:
            if type(e) == ClassicalLiteral:
                left_part = e
            elif e == "_COLON_":
                foundColon = True
            elif type(e) == NafLiteral:
                if foundColon:
                    right_part = e            
                       
        return ChoiceElement(left_part, right_part)
  
    def body(self, elem):                    
        bodyElements = []

        for e in elem:            
            if type(e) == NafLiteral:
                bodyElements.append(e)            
            else:
                for e1 in e:
                    if type(e1) == NafLiteral:
                        bodyElements.append(e1)
                                         
        return bodyElements

        
    def statement(self, elem):    
        foundIf = False        
        head = None
        body = None
        for e in elem:             
            if type(e) == Disjunction or type(e) == Choice:
                head = e
            elif e == "_IF_":
                foundIf = True
            elif type(e) == list:
                if foundIf:
                    body = Conjunction(e)
        self.__rules_list.append(Rule(head, body))                
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
    def hasVariables(self):        
        for term in self.terms:
            if term.isVariable():
                return True
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
class ChoiceElement:
    left_part: ClassicalLiteral
    right_part: NafLiteral
    def toString(self):
        text = StringIO()           
        text.write(self.left_part.toString())
        if self.right_part is not None:
            text.write(":")
            text.write(self.right_part.toString())
        return text.getvalue()


@dataclass(frozen=True)
class Choice:
    lowerGuard: Term  
    upperGuard: Term
    lowerOp: str
    upperOp: str
    elements: list[ChoiceElement]
    def toString(self):
        text = StringIO()
        if self.lowerGuard is not None:
            text.write(self.lowerGuard.name)
            text.write(" ")
            text.write(self.lowerOp)
            text.write(" ")
        text.write("{")
        startedElems = False
        for ce in self.elements:
            if startedElems:
                text.write(";")
            else:
                startedElems = True
            text.write(ce.toString())
        text.write("}")
        if self.upperGuard is not None:
            text.write(" ")
            text.write(self.upperOp)
            text.write(" ")
            text.write(self.upperGuard.name)                      
        return text.getvalue()

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
    head: Disjunction | Choice
    body: Conjunction
    def isFact(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) == 1 and self.body is None and not self.head.atoms[0].hasVariables()
    def isClassical(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) == 1 and not self.head.atoms[0] == Choice and self.body is not None and len(self.body.literals) > 0
    def isStrongConstraint(self):
        return type(self.head) != Choice and self.head is None and self.body is not None and len(self.body.literals) > 0
    def isDisjunctive(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) > 1 and self.body is not None and len(self.body.literals) > 0
    def isChoice(self):
        return type(self.head) == Choice and self.body is not None and len(self.body.literals) > 0

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
