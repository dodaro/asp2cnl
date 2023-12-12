import lark
from lark import Transformer, Discard, Lark
from dataclasses import dataclass
from typing import TextIO

from io import StringIO
import os

class ASPParser:    
    __aspCoreParser = Lark(open(os.path.join(os.path.dirname(__file__), "asp_core_2_grammar/asp_grammar.lark"), "r").read())
    __programFile = None

    def __init__(self, programFile: TextIO):
        self.__programFile = programFile

    def parse(self):
        content_tree: ASPContentTree = ASPTransformer().transform(self.__aspCoreParser.parse(self.__programFile))
        #print(content_tree)
        definitions = [content_tree.rules[i] for i in range(len(content_tree.rules))]
        return definitions

class ASPTransformer(Transformer):
    __rules_list = []
                
    def start(self, elem):   
        tree = ASPContentTree(self.__rules_list[:])  
        __rules_list = []
        return tree
    
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
        #if len(elem) == 1:
        #    classicalLit = ClassicalLiteral(elem[0].value, [])                                     
        #else:                      
        classicalLit = ClassicalLiteral(elem[0].value, elem[2][:])                                     
        return classicalLit

    def aggregate(self, elem):         
        lowerGuard = None
        upperGuard = None
        lowerOp = None
        upperOp = None
        aggregateFunction = None
        foundCurlyOpen = False
        foundCurlyClose = False
        aggregateElements = None
        for e in elem:
            if type(e) == list:
                if not foundCurlyOpen:
                    lowerGuard = e[0]
                    lowerOp = e[1]
                else:
                    aggregateElements = e
            elif self.__isAggrageteFunction__(e):
                aggregateFunction = e
            elif e == '_CURLY_OPEN_':
                foundCurlyOpen = True
            elif e == '_CURLY_CLOSE_':
                foundCurlyClose = True
            elif type(e) == str and foundCurlyClose:
                upperOp = e
            elif type(e) == Term and foundCurlyClose:
                upperGuard = e

        return AggregateLiteral(lowerGuard,upperGuard, lowerOp, upperOp, aggregateFunction, aggregateElements)

       
    def aggregate_function(self, elem): 
        return elem[0].value

    def aggregate_elements(self, elem): 
        aggElements = []
        for e in elem:            
            if type(e) == AggregateElement:
                aggElements.append(e)            
            else:              
                for e1 in e:
                    if type(e1) == AggregateElement:  
                        aggElements.append(e1)                              
        return aggElements

    def aggregate_element(self, elem): 
        aggregateTerms = elem[0]
        aggregateBody = Conjunction(elem[2])
        return AggregateElement(aggregateTerms, aggregateBody)        
    
    def naf_literals(self, elem):
        lits = []
        for t in elem:
            if type(t) == NafLiteral:
                lits.append(t)
            else:              
                for t1 in t:
                    if type(t1) == NafLiteral:  
                        lits.append(t1)        
        return lits

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
    
    def WCONS(self, elem):
        return "_WEAK_IF_"
    def AT(self, elem):
        return "_AT_"
    def MINUS(self, elem):
        return "_MINUS_"

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
            #elif type(e) == NafLiteral:
            elif type(e) == list:
                if foundColon:
                    right_part = e            
                       
        return ChoiceElement(left_part, right_part)
  
    def weight_at_level(self, elem):          
        beforeAtTerm = None
        afterAtTerms = None
        foundAt = False
        foundMinus = False
        for e in elem:
            if e == "_AT_":
                foundAt = True            
            elif e == "_MINUS_":
                foundMinus = True
            else:
                if not foundAt:
                    beforeAtTerm = e
                else:       
                    eToCheck = []             
                    if type(e) == list:
                        eToCheck = e
                    else:
                        eToCheck.append(e)
                    for e1 in eToCheck:
                        if type(e1) == Term:
                            if afterAtTerms is None:
                                afterAtTerms = []                    
                            afterAtTerms.append(e1)                    
        return WeakElement(beforeAtTerm, afterAtTerms, foundMinus)

    
    def body(self, elem):                
        bodyElements = []

        for e in elem:            
            if type(e) == NafLiteral or type(e) == AggregateLiteral:
                bodyElements.append(e)           
            else:                
                for e1 in e:
                    if type(e1) == NafLiteral or type(e1) == AggregateLiteral:
                        bodyElements.append(e1)
                                         
        return bodyElements
    
    def body_choice_suchthat(self, elem):                
        bodyElements = []

        for e in elem:            
            if type(e) == NafLiteral:
                bodyElements.append(e)           
            elif type(e) == list:                      
                for e1 in e:
                    if type(e1) == NafLiteral:
                        bodyElements.append(e1)
                                         
        return bodyElements

        
    def statement(self, elem):    
        foundIf = False        
        head = None
        body = None
        weakElement = None
        for e in elem:             
            if type(e) == Disjunction or type(e) == Choice:
                head = e
            elif e == "_IF_" or e == "_WEAK_IF_":
                foundIf = True
            elif type(e) == list:
                if foundIf:
                    body = Conjunction(e)
            elif type(e) == WeakElement:
                weakElement = e

        self.__rules_list.append(Rule(head, body, weakElement))                
        return elem    

    def __isAggrageteFunction__(self, value):     
        return value == "#min" or value == "#max" or value == "#sum" or value == "#count" # ecc

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
class AggregateElement:
    leftTerms: list[Term]
    body: 'Conjunction'
    def toString(self):        
        text = StringIO()
        started = False
        for t in self.leftTerms:
            if started:
                text.write(",")
                text.write(" ")
            else:
                started = True
            text.write(t.toString())
        text.write(":")
        text.write(" ")
        text.write(self.body.toString())
        return text.getvalue()


@dataclass(frozen=True)
class AggregateLiteral:
    lowerGuard: Term  
    upperGuard: Term
    lowerOp: str
    upperOp: str
    aggregateFunction: str
    aggregateElement: list[AggregateElement]
    def toString(self):        
        text = StringIO()
        if self.lowerGuard is not None:
            text.write(self.lowerGuard.toString())
            text.write(" ")
            text.write(self.lowerOp)
            text.write(" ")
        text.write(self.aggregateFunction)
        text.write("{")
        started = False
        for aggrEl in self.aggregateElement:
            if started:
                text.write(";")
                text.write(" ")
            else:
                started = True
            text.write(aggrEl.toString())
        text.write("}")
        if self.upperGuard is not None:
            text.write(" ")
            text.write(self.upperOp)
            text.write(" ")
            text.write(self.upperGuard.toString())
            text.write(" ")
        return text.getvalue()            

@dataclass(frozen=True)
class Conjunction:
    literals: list[NafLiteral | AggregateLiteral] 
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
        return text.getvalue()


@dataclass(frozen=True)
class ChoiceElement:
    left_part: ClassicalLiteral
    right_part: list[NafLiteral]
    def toString(self):
        text = StringIO()           
        text.write(self.left_part.toString())
        if self.right_part is not None:
            text.write(":")
            started = False
            for nafLit in self.right_part:
                if started:
                    text.write(",")
                    text.write(" ")
                else:
                    started = True
                text.write(nafLit.toString())
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
class WeakElement:    
    beforeAt: Term
    afterAt: list[Term]
    isMaximize: bool = False
    def toString(self):
        text = StringIO() 
        text.write("[")
        if self.beforeAt is not None:
            if (self.isMaximize):
                text.write("-")
            text.write(self.beforeAt.toString())
        if self.afterAt is not None:
            text.write("@")
            started = False
            for elem in self.afterAt:
                if started:
                    text.write(",")
                else:
                    started = True
                text.write(elem.toString())
        text.write("]")
        return text.getvalue()


@dataclass(frozen=True)
class Rule:
    head: Disjunction | Choice
    body: Conjunction
    weight_at_level: WeakElement = None
    def isFact(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) == 1 and self.body is None and not self.head.atoms[0].hasVariables()
    def isClassical(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) == 1 and not self.head.atoms[0] == Choice and self.body is not None and len(self.body.literals) > 0
    def isStrongConstraint(self):
        return type(self.head) != Choice and self.head is None and self.body is not None and len(self.body.literals) > 0 and self.weight_at_level is None
    def isDisjunctive(self):
        return type(self.head) != Choice and self.head is not None and len(self.head.atoms) > 1 and self.body is not None and len(self.body.literals) > 0
    def isChoice(self):
        return type(self.head) == Choice and self.body is not None and len(self.body.literals) > 0
    def isWeakConstraint(self):
        return type(self.head) != Choice and self.head is None and self.body is not None and len(self.body.literals) > 0 and self.weight_at_level is not None

    def toString(self):
        text = StringIO() 
        if self.head is not None:
            text.write(self.head.toString())
        if self.body is None:
            text.write(".")
        else:
            if self.isWeakConstraint():
                text.write(" :~ ")
            else:
                text.write(" :- ")
            text.write(self.body.toString())
        text.write(".")
        if self.isWeakConstraint():
            text.write(" ")
            text.write(self.weight_at_level.toString())
        return text.getvalue()
            
  
@dataclass(frozen=True)
class ASPContentTree:
    rules: list
