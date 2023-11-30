from io import StringIO

import sys
import os
ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl/cnl2asp/'
sys.path += [ROOT_CNL2ASP_PATH + 'src']

from cnl2asp.cnl2asp import Symbol

from asp2cnl.parser import ClassicalLiteral, BuiltinAtom, NafLiteral, AggregateLiteral

def extract_name(name):
    if type(name) == Symbol:
        return extract_name(name.predicate)
    return name 

def get_symbol(symbols, symbol_name):    
    symbol_name = symbol_name.replace("_", " ")
    res: list = [symbols[i] for i in
                            range(len(symbols)) if
                            symbols[i].predicate == symbol_name]      
    if len(res) == 0:
        return None
    else:
        for i in range(len(res[0].attributes)):
            if type(res[0].attributes[i]) == Symbol:
                res[0].attributes[i] = res[0].attributes[i].predicate# + "_" + res[0].attributes[0]                

        return res[0]

def compile(rule, symbols):    
    results = StringIO()
    if rule.isFact():    
        #Facts    
        atom = rule.head.atoms[0]       
        symb = get_symbol(symbols, atom.name)             
        if len(atom.terms) == 1:
            if symb is None:
                results.write(generate_is_a(atom))            
            else:                
                results.write(generate_there_is(atom, symb, {}, True))            
            results.write(".")
            results.write("\n")                                                   

        elif len(atom.terms) >= 2:              
            if symb is not None:
                results.write(generate_there_is(atom, symb, {}, True)) 
                results.write(".")  
                results.write("\n")           
            #else:
            #    results.write(generate_relation(atom)) 
            #    results.write("\n")
    elif rule.isClassical():            
        results.write(generate_classical_statement(rule, symbols))   
        results.write("\n")    
    elif rule.isStrongConstraint():
        results.write(generate_strong_constraint(rule, symbols))
        results.write("\n") 
    elif rule.isDisjunctive() or rule.isChoice():
        results.write(generate_disjunctive_or_choice_statement(rule, symbols))
        results.write("\n") 
    elif rule.isWeakConstraint():
        results.write(generate_weak_constraint(rule, symbols))
        results.write("\n") 
        
    return results.getvalue()

def generate_is_a(atom):
    #Eg. pub(1). --> 1 is a pub.
    results = StringIO()    
    results.write(atom.terms[0].name.replace('"', '').capitalize()) 
    results.write(" ")
    results.write("is a") 
    results.write(" ")
    results.write(atom.name)                     
    return results.getvalue()

def generate_there_is(atom, symbol, builtinAtoms, start = False):
    #Eg. movie(1,"jurassicPark","spielberg",1993).
    # -->
    #There is a movie with id equal to 1, with director equal to spielberg, with title equal to jurassicPark, with year equal to 1993.
    isNot = False
    if type(atom) == NafLiteral:
        isNot = atom.isNot
        atom = atom.literal
    results = StringIO()
    if start:
        results.write("There") 
    else:
        results.write("there") 
    results.write(" ")
    results.write("is")
    results.write(" ")
    if isNot:
        results.write("not")
        results.write(" ")
    results.write("a") 
    results.write(" ")
    results.write(atom.name)
    results.write(" ")
    results.write(generate_with(atom, symbol, builtinAtoms))
    return results.getvalue()
    
     
def generate_with(atom, symbol, builtinAtoms = {}):
    results = StringIO()
    started = False
    for i in range(len(atom.terms)):
        if not atom.terms[i].isUnderscore():                         
            if started:
                results.write(", ")
            else:
                started = True    
                #results.write(" ")
            results.write("with")
            results.write(" ")              

            results.write(symbol.attributes[i])
            results.write(" ")
            if atom.terms[i].isVariable(): 
                if atom.terms[i] in builtinAtoms.keys():    
                    results.write(atom.terms[i].name)
                    results.write(" ")                      
                    builtinAtom = builtinAtoms[atom.terms[i]]
                    results.write(generate_compare_operator_sentence(builtinAtom.op))
                    results.write(" ")    

                    results.write(builtinAtom.terms[1].name)                       
                else:
                    results.write(atom.terms[i].name)  
            else:                                                        
                results.write("equal")   
                results.write(" ")
                results.write("to")   
                results.write(" ")
                results.write(atom.terms[i].name.strip('\"')) 

        #results.write(extract_name(symbol.attributes[i]))
        #results.write(" ")   
        #results.write("equal to")
        #results.write(" ")
        #results.write(atom.terms[i].name.strip('\"'))    
    return results.getvalue()

def generate_compare_operator_sentence(operator):
    results = StringIO()
    if operator == "!=" or operator == "<>":
        # different from
        results.write("different")   
        results.write(" ")
        results.write("from")                               
    elif operator == "<":
        # less than
        results.write("less")   
        results.write(" ")
        results.write("than")           
    elif operator == "<=":
        # less than or equal to
        results.write("less")   
        results.write(" ")
        results.write("than")   
        results.write(" ")
        results.write("or")   
        results.write(" ")
        results.write("equal")   
        results.write(" ")
        results.write("to")           
    elif operator == "=":
        # equal to    
        results.write("equal")   
        results.write(" ")
        results.write("to")           
    elif operator == ">":
        # greater than    
        results.write("greater")   
        results.write(" ")
        results.write("than")           
    elif operator == ">=":
        # greater than or equal to   
        results.write("greater")   
        results.write(" ")
        results.write("than")   
        results.write(" ")
        results.write("or")   
        results.write(" ")
        results.write("equal")   
        results.write(" ")
        results.write("to")       
    elif operator == "between":    
        results.write("between")    
    return results.getvalue()

#TODO

def generate_relation(atom):
    #Eg. work_in("john",1). 
    #--> Waiter John works in pub 1.
    # serve("john","alcoholic").
    # --> Waiter John serves a drink alcoholic.
    results = StringIO()                                        
    #symb = get_symbol(symbols, atom.name.replace("_", " "))
    #atom_name = atom.name.replace("_", " ")
    atom_name = atom.name

    #symb = get_symbol(symbols, atom.terms[0])
    #if symb is not None: 
        #results.write(symb.predicate('"', '').capitalize())
        #results.write(" ")    
    results.write(atom.terms[0].name.replace('"', ''))
    results.write(" ")
    results.write(atom_name)
    for i in range(len(atom.terms)):
        if i > 0:
            results.write(" ")
            results.write("and")    
        results.write(" ")
        results.write(atom.terms[i].name.replace('"', ''))
        #symb2 = get_symbol(symbols, atom.terms[1])

    
    '''
    for i in range(len(atom.terms)):
        symb = get_symbol(symbols, atom.name)
        if symb is not None:            
            results.write(atom.terms[i].replace('"', '').capitalize())
    
    results.write(symb.predicate)
    results.write(" ")
    results.write(atom.terms[1].replace('"', ''))
    '''
    results.write(".")

    return results.getvalue()


def generate_disjunctive_or_choice_statement(rule, symbols):
    # DISJUNCTIVE
    # Eg. scoreassignment(movie(I),1) | scoreassignment(movie(I),2) 
    #               | scoreassignment(movie(I),3) :- movie(I,_,_,_).
    # -->
    # Whenever there is a movie with id I, we can have with director equal to spielberg
    # a scoreAssignment with movie I, and with value equal to 1 
    # or a scoreAssignment with movie I, and with value equal to 2 
    # or a scoreAssignment with movie I, and with value equal to 3. 
    # -------
    # CHOICE
    # Eg. 0 <= {topmovie(I):movie(I,_,X,_)} <= 1 :- director(X), X != spielberg.
    # -->
    # Whenever there is a director with name X different from spielberg 
    #         then we can have at most 1 topmovie with id I such that there is a movie with director X, 
    #           and with id I.   
    results = StringIO()        
    results.write(generate_body(rule.body, symbols))    
    results.write(" ")
    results.write("then") 
    results.write(" ")
    results.write("we") 
    results.write(" ")
    results.write("can") 
    results.write(" ")
    results.write("have") 
    results.write(" ")

    if rule.isChoice():
        results.write(generate_head_choice(rule.head, symbols))
    else:
        results.write(generate_head(rule.head, symbols))
    
    results.write(".")
    return results.getvalue()

def generate_classical_statement(rule, symbols):
    # Eg. topmovie(X) :- movie(X,_,"spielberg",_).
    # -->
    # Whenever there is a movie with id X, with director equal to spielberg
    # then we must have a topmovie with id X.    
    results = StringIO()        
    results.write(generate_body(rule.body, symbols))    
    results.write(" ")
    results.write("then") 
    results.write(" ")
    results.write("we") 
    results.write(" ")
    results.write("must") 
    results.write(" ")
    results.write("have") 
    results.write(" ")

    results.write(generate_head(rule.head, symbols))
    results.write(".")
    return results.getvalue()

def generate_strong_constraint(rule, symbols):
    # Eg. :- movie(X,_,_,1964), topmovie(Y), X = Y.
    # -->
    # It is prohibited that X is equal to Y, whenever there is a movie 
    # with id X, and with year equal to 1964, whenever there is a topMovie with id Y.
    results = StringIO()  
    results.write("It is prohibited that")     
    results.write(generate_body(rule.body, symbols, True)) 
    results.write(".") 
    return results.getvalue()  

def generate_weak_constraint(rule, symbols):
    results = StringIO()  
    results.write("It is preferred")
    if rule.weight_at_level.afterAt is not None:
        results.write(", ")
        results.write("with")
        results.write(" ")
        if rule.weight_at_level.afterAt[0].name == "1":
            results.write("low")
            results.write(" ")
        elif rule.weight_at_level.afterAt[0].name == "2":
            results.write("medium")
            results.write(" ")
        elif rule.weight_at_level.afterAt[0].name == "3":            
            results.write("high")
            results.write(" ")
        results.write("priority")
        results.write(",")
    results.write(" ")
    results.write("that")
    #results.write(" ")
    
    results.write(generate_body(rule.body, symbols, False, rule.weight_at_level.beforeAt)) 
    
    #results.write(", ") 
    #results.write(rule.weight_at_level.beforeAt.name)
    #results.write(" ") 
    results.write("is")
    results.write(" ")
    results.write("minimized")   
    results.write(".") 
    return results.getvalue()  

def generate_head_choice(head, symbols):
    results = StringIO() 
    atMost = False   
    atLeast = False 
    beetween = False    
    exactly = False   
    if head.upperGuard is not None:
        if head.upperOp == "<=":
            if head.lowerGuard is None:
                atMost = True
            else:
                if head.lowerOp == "<=":
                    if head.lowerGuard.name == head.upperGuard.name:
                        exactly = True
                    elif int(head.lowerGuard.name) < int(head.upperGuard.name):
                        beetween = True 
        elif head.upperOp == "=":
            if head.lowerGuard is None:
                exactly = True
            else:
                if head.lowerOp == "=":
                    if head.lowerGuard.name == head.upperGuard.name:
                        exactly = True
    else:
        if head.lowerGuard is not None:
            if head.lowerOp == "=":
                exactly = True
            elif head.lowerOp == "<=":
                atLeast = True
    if exactly:
        # exactly 1 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        results.write("exactly")
        results.write(" ")
        if head.lowerGuard is not None:            
            results.write(head.lowerGuard.name)
        else:
            results.write(head.upperGuard.name)
    if atLeast:
        # at least 1 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        results.write("at least")
        results.write(" ")
        results.write(head.lowerGuard.name)
    if atMost:
        # at most 1 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        results.write("at most")
        results.write(" ")
        results.write(head.upperGuard.name)
    if beetween:
        # between 3 and 4 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        results.write("between")
        results.write(" ")
        results.write(head.lowerGuard.name)
        results.write(" ")
        results.write("and")
        results.write(" ")
        results.write(head.upperGuard.name)
    results.write(" ")
    results.write(head.elements[0].left_part.name)
    results.write(" ")
    results.write(generateWith(symbols, head.elements[0].left_part))  
    results.write(" ")
    results.write("such that")
    results.write(" ")
    symb = get_symbol(symbols, head.elements[0].right_part.literal.name)
    results.write(generate_there_is(head.elements[0].right_part, symb, {}))

    # lowerGuard: Term  
    # upperGuard: Term
    # lowerOp: str
    # upperOp: str
    # elements: list[ChoiceElement]
    return results.getvalue()  

def generate_head(head, symbols):
    results = StringIO() 
    started = False
    for atom in head.atoms:
        if started:
            results.write(" ")
            results.write("or")
            results.write(" ")
        else:
            started = True
        results.write("a")
        results.write(" ")
        results.write(atom.name)
        results.write(" ")  

        results.write(generateWith(symbols, atom))         
              
    return results.getvalue()


def generateWith(symbols, atom):
    results = StringIO() 
    symbLit = get_symbol(symbols, atom.name)
        
    for i in range(len(symbLit.attributes)):
        if i > 0:
            results.write(",")   
            results.write(" ")
        results.write("with")   
        results.write(" ")
        results.write(symbLit.attributes[i])
        results.write(" ")

        if not atom.terms[i].isVariable():                                    
            results.write("equal")   
            results.write(" ")
            results.write("to")   
            results.write(" ")
        results.write(atom.terms[i].name.strip('\"'))   
        #results.write(" ")  
    return results.getvalue()

def generate_body(body, symbols, isStrongConstraint = False, costWeakTerm = None):
    results = StringIO()   
    startedLits = False 
    # Find builtins
    builtinAtoms = {}
    
    for lit in body.literals: 
        if type(lit) == NafLiteral and type(lit.literal) == BuiltinAtom:            
            builtinAtoms[lit.literal.terms[0]] = lit.literal
    
    tmpWheneverResults = None 
    tmpAggrResults = None
    foundAggr = None
    firstConstraintLiteralInSentence = None    
    specialConstraintTranslationForLiteral = False
    for lit in body.literals:    
        if type(lit) == NafLiteral and type(lit.literal) == ClassicalLiteral:  
            if tmpWheneverResults is None:
                tmpWheneverResults = StringIO()  
            if startedLits:
                tmpWheneverResults.write(",")   
                tmpWheneverResults.write(" ")
                tmpWheneverResults.write("whenever")
            else:  
                if not isStrongConstraint:
                    tmpWheneverResults.write("Whenever")
                else:                    
                    specialConstraintTranslationForLiteral = True

                #if costWeakTerm is not None:      
                #    tmpWheneverResults.write(" ")              
                #    tmpWheneverResults.write("whenever")         
                #elif not isStrongConstraint:
                #    tmpWheneverResults.write("Whenever")   
                startedLits = True
            symbLit = get_symbol(symbols, lit.literal.name)
            if not specialConstraintTranslationForLiteral:                
                tmpWheneverResults.write(" ")                            
                tmpWheneverResults.write(generate_there_is(lit, symbLit, builtinAtoms))
            else:
                specialConstraintTranslationForLiteral = False                
                firstConstraintLiteralInSentence = " " + generate_there_is(lit, symbLit, builtinAtoms)
            #tmpWheneverResults.write(" ")
        elif type(lit) == AggregateLiteral:
            foundAggr = lit                        
            #aggregate = lit

            #operator = getAggregateOperator(aggregate)
            #if operator == "=":    
            #    if (aggregate.lowerOp == "=" and aggregate.upperGuard is None) or (aggregate.upperOp == "=" and aggregate.lowerGuard is None):
            #        if aggregate.upperGuard is not None and aggregate.upperGuard.isVariable():
            #            assignmentVar = aggregate.upperGuard
            #        elif aggregate.lowerGuard is not None and aggregate.lowerGuard.isVariable():
            #            assignmentVar = aggregate.lowerGuard
                            
            if not isStrongConstraint and costWeakTerm is None:
                if startedLits:
                    results.write("whenever")
                else:
                    results.write("Whenever")
                    startedLits = True
                results.write(" ")
                results.write("we have that")
                #results.write(" ") 
                
            results.write(" ")
            results.write(generate_aggregate_subsentence(lit, symbols, costWeakTerm, isStrongConstraint))
            startedLits = True
    #if foundAggr is not None and tmpWheneverResults is not None:
    #    results.write(" ")
    #    results.write("whenever")
    
    needVariable = False

    if foundAggr is None:
        needVariable = True
    else:
        if (foundAggr.lowerOp == "=" and foundAggr.upperGuard is None) or (foundAggr.upperOp == "=" and foundAggr.lowerGuard is None):
            if foundAggr.upperGuard is not None and foundAggr.upperGuard.isVariable():
                needVariable = True
            elif foundAggr.lowerGuard is not None and foundAggr.lowerGuard.isVariable():
                needVariable = True

    if tmpWheneverResults is not None:
        if costWeakTerm is not None and needVariable:        
            tmpWheneverResults.write(", ") 
            tmpWheneverResults.write(costWeakTerm.name)  
            tmpWheneverResults.write(" ") 

        if firstConstraintLiteralInSentence is not None:
            if foundAggr is not None:
                results.write(" whenever " + firstConstraintLiteralInSentence)
            else:
                results.write(firstConstraintLiteralInSentence)
        results.write(tmpWheneverResults.getvalue())
                                               
    return results.getvalue()

def getAggregateOperator(aggregate):
    operator = None
    if (aggregate.lowerOp == "=" and aggregate.upperGuard is None
                    or aggregate.upperOp == "=" and aggregate.lowerGuard is None
                    or aggregate.lowerOp == "=" and aggregate.upperOp == "="
                            and aggregate.lowerGuard.name == aggregate.upperGuard.name
                    or aggregate.lowerOp == "<=" and aggregate.upperOp == "<="
                            and aggregate.lowerGuard.name == aggregate.upperGuard.name
                    or aggregate.lowerOp == ">=" and aggregate.upperOp == ">="
                            and aggregate.lowerGuard.name == aggregate.upperGuard.name
                    ):
        operator = "="
        if (aggregate.lowerOp == "=" and aggregate.upperGuard is None) or (aggregate.upperOp == "=" and aggregate.lowerGuard is None):
            if aggregate.upperGuard is not None and aggregate.upperGuard.isVariable():
                assignmentVar = aggregate.upperGuard
            elif aggregate.lowerGuard is not None and aggregate.lowerGuard.isVariable():
                assignmentVar = aggregate.lowerGuard
                
    elif (aggregate.upperOp == ">" and aggregate.lowerGuard is None):
        operator = ">"
    elif (aggregate.upperOp == ">=" and aggregate.lowerGuard is None):
        operator = ">="
    elif (aggregate.upperOp == "<" and aggregate.lowerGuard is None):
        operator = "<"
    elif (aggregate.upperOp == "<=" and aggregate.lowerGuard is None):
        operator = "<="    
    elif (aggregate.lowerOp == "<=" and aggregate.upperOp == "<="):
        operator = "between" 
    #    results.write("beet")
    return operator

def generate_aggregate_subsentence(aggregate, symbols, costWeakTerm = None, isStrongConstraint = True):
    results = StringIO()     
    # #AGGR{VL, X: scoreassignment(X,VL)} = 1
    # --->
    # the lowest value of a scoreAssignment with movie id X for each id is equal to 1        
    

    operator = None
    assignmentVar = None
    operator = getAggregateOperator(aggregate)
    if operator == "=":    
        if (aggregate.lowerOp == "=" and aggregate.upperGuard is None) or (aggregate.upperOp == "=" and aggregate.lowerGuard is None):
            if aggregate.upperGuard is not None and aggregate.upperGuard.isVariable():
                assignmentVar = aggregate.upperGuard
            elif aggregate.lowerGuard is not None and aggregate.lowerGuard.isVariable():
                assignmentVar = aggregate.lowerGuard
                    
    if operator is not None:                
        if (costWeakTerm is not None and assignmentVar is not None and costWeakTerm.name == assignmentVar.name
                or isStrongConstraint):
            results.write("")
        else:
            if costWeakTerm is not None:
                results.write("whenever")
                results.write(" ")
                results.write("we have that")
                results.write(" ")     
     

    aggrTerm = aggregate.aggregateElement[0].leftTerms[0]
    forEachTerms = aggregate.aggregateElement[0].leftTerms[1:]     
    forEachSubsentences = None
    if len(aggregate.aggregateElement[0].leftTerms) > 1:
        forEachSubsentences = [None] * (len(aggregate.aggregateElement[0].leftTerms) - 1)
    foundClassicalLiteral = None
    foundVarOfLiteral = None
    positionOfFoundVar = -1
    for naf_literal in aggregate.aggregateElement[0].body.literals:
        #if foundClassicalLiteral is None:
            if type(naf_literal) == NafLiteral:
                if type(naf_literal.literal) == ClassicalLiteral:
                    p = 0
                    for t in naf_literal.literal.terms:
                        if t.name == aggrTerm.name:
                            foundClassicalLiteral = naf_literal.literal
                            foundVarOfLiteral = t
                            positionOfFoundVar = p
                        if t in forEachTerms:
                            subEach = StringIO() 
                            subEach.write("for each")
                            subEach.write(" ")
                            symbLit = get_symbol(symbols, naf_literal.literal.name)          
                            subEach.write(symbLit.attributes[p])  
                            forEachSubsentences[forEachTerms.index(t)] = subEach.getvalue()
                        p = p + 1
    
    connective = None
    if foundClassicalLiteral is not None:
        results.write("the")
        results.write(" ")
        if aggregate.aggregateFunction == "#min":
            results.write("lowest")
            connective = "of"
        elif aggregate.aggregateFunction == "#max":
            results.write("highest")   
            connective = "of"         
        elif aggregate.aggregateFunction == "#count":
            results.write("number of")  
            connective = "that have"
        elif aggregate.aggregateFunction == "#sum":
            results.write("total")  
            connective = "that have"
            #connective = "of"
        results.write(" ")      
        symbLit = get_symbol(symbols, foundClassicalLiteral.name)          
        results.write(symbLit.attributes[positionOfFoundVar])  
        #results.write(" ") 

        if forEachSubsentences is not None:                        
            for s in forEachSubsentences:
                results.write(", ")
                results.write(s)
                results.write(", ")
        else:
            results.write(" ")

        if connective is not None:
            results.write(connective)
        results.write(" ") 
        results.write("a")  
        results.write(" ") 
        results.write(foundClassicalLiteral.name)
        results.write(" ") 

        tmpLitTerm = foundClassicalLiteral.terms.pop(positionOfFoundVar)
        tmpSymbTerm = symbLit.attributes.pop(positionOfFoundVar)
        results.write(generate_with(foundClassicalLiteral, symbLit))
        #results.write(" ") 
        foundClassicalLiteral.terms.insert(positionOfFoundVar, tmpLitTerm)
        symbLit.attributes.insert(positionOfFoundVar, tmpSymbTerm)


        if len(aggregate.aggregateElement[0].body.literals) > 1: 
            #results.write("in")
            results.write(" ")
            startedIn = False
            for nafLit in aggregate.aggregateElement[0].body.literals[1:]:
                if startedIn:
                    results.write(",")
                    results.write(" ")
                else:
                    startedIn = True
                results.write(nafLit.literal.name)
                results.write(" ")
                results.write(nafLit.literal.terms[0].name)
            results.write(" ") 

        if operator is not None:            
            if costWeakTerm is not None and assignmentVar is not None and costWeakTerm.name == assignmentVar.name:
                results.write("")
            else:                
                results.write(" ") 
                results.write("is") 
                results.write(" ") 
                results.write(generate_compare_operator_sentence(operator))  
                results.write(" ") 
                if operator == "between":
                    results.write(aggregate.lowerGuard.name)  
                    results.write(" ") 
                    results.write("and") 
                    results.write(" ") 
                    results.write(aggregate.upperGuard.name)  
                else:
                    if aggregate.lowerGuard is not None:
                        results.write(aggregate.lowerGuard.name)  
                    else:
                        results.write(aggregate.upperGuard.name)   
                
                     
    return results.getvalue()
            

'''
    @dataclass(frozen=True)
class AggregateElement:
    leftTerms: list[Term]
    body: 'Conjunction'

@dataclass(frozen=True)
class Aggregate:
    lowerGuard: Term  
    upperGuard: Term
    lowerOp: str
    upperOp: str
    aggregateFunction: str
    aggregateElement: list[AggregateElement]
'''
