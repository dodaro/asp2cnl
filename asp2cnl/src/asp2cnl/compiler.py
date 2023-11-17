from io import StringIO

import sys
ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl2asp/cnl2asp/'
sys.path += [ROOT_CNL2ASP_PATH + 'src']
from cnl2asp.cnl2asp import Symbol

from asp2cnl.parser import ClassicalLiteral, BuiltinAtom, NafLiteral

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
        return res[0]

def compile(rule, symbols):    
    results = StringIO()
    if rule.isFact():        
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
    started = False
     
    for i in range(len(atom.terms)):
        if not atom.terms[i].isUnderscore():                         
            if started:
                results.write(", ")
            else:
                started = True    
            results.write("with")
            results.write(" ")              

            results.write(symbol.attributes[i])
            results.write(" ")
            if atom.terms[i].isVariable(): 
                if atom.terms[i] in builtinAtoms.keys():    
                    results.write(atom.terms[i].name)
                    results.write(" ")                      
                    builtinAtom = builtinAtoms[atom.terms[i]]
                    if builtinAtom.op == "!=" or builtinAtom.op == "<>":
                        # different from
                        results.write("different")   
                        results.write(" ")
                        results.write("from")   
                        results.write(" ")                                
                    elif builtinAtom.op == "<":
                        # less than
                        results.write("less")   
                        results.write(" ")
                        results.write("than")   
                        results.write(" ")
                    elif builtinAtom.op == "<=":
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
                        results.write(" ")
                    elif builtinAtom.op == "=":
                        # equal to    
                        results.write("equal")   
                        results.write(" ")
                        results.write("to")   
                        results.write(" ")
                    elif builtinAtom.op == ">":
                        # greater than    
                        results.write("greater")   
                        results.write(" ")
                        results.write("than")   
                        results.write(" ")
                    elif builtinAtom.op == ">=":
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

def generate_body(body, symbols, isContraint = False):
    results = StringIO()   
    startedLits = False 
    # Find builtins
    builtinAtoms = {}
    
    for lit in body.literals: 
        if type(lit.literal) == BuiltinAtom:            
            builtinAtoms[lit.literal.terms[0]] = lit.literal
    
    for lit in body.literals:    
        if type(lit.literal) == ClassicalLiteral:    
            if startedLits:
                results.write(",")   
                results.write(" ")
                results.write("whenever")
            else:        
                if not isContraint:                        
                    results.write("Whenever")   
                startedLits = True
            results.write(" ")

            symbLit = get_symbol(symbols, lit.literal.name)
            results.write(generate_there_is(lit, symbLit, builtinAtoms))

            '''
            results.write("there")   
            results.write(" ")
            results.write("is")   
            results.write(" ")
            if lit.isNot:
                results.write("not")   
                results.write(" ")
            #if type(lit.classical_literal) == ClassicalLiteral:
        
            
            results.write("a")   
            results.write(" ")
            results.write(lit.literal.name)   
            results.write(" ")
            startedTerms = False
            for i in range(len(symbLit.attributes)):                                
                if not lit.literal.terms[i].isUnderscore():                         
                    if startedTerms:
                        results.write(",")   
                        results.write(" ")
                    else:
                        startedTerms = True
                    results.write("with")   
                    results.write(" ")
                    results.write(symbLit.attributes[i])
                    results.write(" ")
                    if lit.literal.terms[i].isVariable(): 
                        if lit.literal.terms[i] in builtinAtoms.keys():    
                            results.write(lit.literal.terms[i].name)
                            results.write(" ")                      
                            builtinAtom = builtinAtoms[lit.literal.terms[i]]
                            if builtinAtom.op == "!=" or builtinAtom.op == "<>":
                                # different from
                                results.write("different")   
                                results.write(" ")
                                results.write("from")   
                                results.write(" ")                                
                            elif builtinAtom.op == "<":
                                # less than
                                results.write("less")   
                                results.write(" ")
                                results.write("than")   
                                results.write(" ")
                            elif builtinAtom.op == "<=":
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
                                results.write(" ")
                            elif builtinAtom.op == "=":
                                # equal to    
                                results.write("equal")   
                                results.write(" ")
                                results.write("to")   
                                results.write(" ")
                            elif builtinAtom.op == ">":
                                # greater than    
                                results.write("greater")   
                                results.write(" ")
                                results.write("than")   
                                results.write(" ")
                            elif builtinAtom.op == ">=":
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
                                results.write(" ")
                            results.write(builtinAtom.terms[1].name)                       
                        else:
                            results.write(lit.literal.terms[i].name)  
                    else:                                                        
                        results.write("equal")   
                        results.write(" ")
                        results.write("to")   
                        results.write(" ")
                        results.write(lit.literal.terms[i].name.strip('\"'))       
            '''                                            
    return results.getvalue()

