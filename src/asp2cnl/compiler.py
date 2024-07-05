from io import StringIO
from cnl2asp.cnl2asp import Symbol, SymbolType

from asp2cnl.parser import Directive, NafLiteral, ClassicalLiteral, Term, ArithmeticAtom, BuiltinAtom, AggregateLiteral


def extract_name(name):
    if type(name) == Symbol:
        return extract_name(name.predicate)
    return name


def get_symbol(symbols, atom):
    symbol_name = atom.name
    res: list = [symbols[i] for i in
                 range(len(symbols)) if
                 symbols[i].predicate.lower() == symbol_name.lower()]

    if len(res) == 0:
        return None
    else:
        symb = None

        for s in res:
            if s.symbol_type == SymbolType.TEMPORAL:
                s.attributes = s.attributes[0:1]
            if len(s.attributes) == atom.arity():
                symb = s

        for i in range(len(symb.attributes)):
            if type(symb.attributes[i]) == Symbol:
                if symb.attributes[i].symbol_type == SymbolType.DEFAULT:
                    symb.attributes[i] = symb.attributes[i].predicate.strip() + " " + (
                        symb.attributes[i].attributes[0].strip()).lower()
                else:
                    symb.attributes[i] = symb.attributes[i].predicate.strip()
            else:
                symb.attributes[i] = symb.attributes[i].strip()
        return symb


def compile_rule(rule, symbols):
    results = StringIO()
    if type(rule) == Directive:
        results.write(generate_directive(rule, symbols))
    else:
        if rule.isFact():
            # Facts
            atom = rule.head.atoms[0]
            symb = get_symbol(symbols, atom)
            if symb is None or symb.symbol_type == SymbolType.DEFAULT:
                if len(atom.terms) == 1:
                    if symb is None:
                        results.write(generate_is_a(atom))
                    else:
                        if atom.terms[0].isWithDotDot():
                            results.write(generate_goes(atom))
                        else:
                            results.write(generate_there_is(atom, symb, {}, True))
                    results.write(".")
                elif len(atom.terms) >= 2:
                    if symb is not None:
                        results.write(generate_there_is(atom, symb, {}, True))
                        results.write(".")
        elif rule.isClassical():
            results.write(generate_classical_statement(rule, symbols))
        elif rule.isStrongConstraint():
            results.write(generate_strong_constraint(rule, symbols))
        elif rule.isDisjunctive() or rule.isChoice():
            results.write(generate_disjunctive_or_choice_statement(rule, symbols))
        elif rule.isWeakConstraint():
            results.write(generate_weak_constraint(rule, symbols))

    return results.getvalue()


def generate_directive(directive, symbols):
    results = StringIO()
    if directive.type == "const":
        results.write(directive.name)
        results.write(" is a constant equal to")
        results.write(" ")
        results.write(directive.value)
        results.write(".")
    return results.getvalue()


def generate_is_a(atom):
    # Eg. pub(1). --> 1 is a pub.
    results = StringIO()
    results.write(atom.terms[0].name.replace('"', '').capitalize())
    results.write(" ")
    results.write("is a")
    results.write(" ")
    results.write(atom.name)
    return results.getvalue()


def generate_goes(atom):
    results = StringIO()
    results.write("A")
    results.write(" ")
    results.write(atom.name)
    results.write(" ")
    results.write("goes")
    results.write(" ")
    results.write("from")
    results.write(" ")
    results.write(atom.terms[0].name)
    results.write(" ")
    results.write("to")
    results.write(" ")
    results.write(atom.terms[0].afterDotDot)
    return results.getvalue()


def generate_there_is(atom, symbol, builtinAtoms, start=False, noThereIs=False, literalVariable=None):
    # Eg. movie(1,"jurassicPark","spielberg",1993).
    # -->
    # There is a movie with id equal to 1, with director equal to spielberg, with title equal to jurassicPark, with year equal to 1993.
    isNot = False
    if type(atom) == NafLiteral:
        isNot = atom.isNot
        atom = atom.literal
    results = StringIO()
    if not noThereIs:
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

    if literalVariable is not None:
        results.write(literalVariable)
        results.write(" ")

    results.write(generate_with(atom, symbol, builtinAtoms))
    return results.getvalue()


def get_literal_identifier(body, lit):
    count = 0
    for l in body.literals:
        if type(l) == NafLiteral and type(l.literal) == ClassicalLiteral:
            if l.literal.name == lit.literal.name:
                count = count + 1
                if l == lit:
                    return lit.literal.name.upper() + str(count)
    return None


def generate_vars_symbols(body, symbols, arithAtom):
    results = StringIO()
    matchedVars = []
    for term in arithAtom.terms:
        if term.isVariable():
            matchedVars.append((term, None, None))
        else:
            matchedVars.append(term)

    foundLitNames = []
    for lit in body.literals:
        if type(lit) == NafLiteral and type(lit.literal) == ClassicalLiteral:
            symbLit = get_symbol(symbols, lit.literal)
            atom = lit.literal
            foundLitNames.append(atom.name)
            for i in range(len(atom.terms)):
                canContinue = True
                if type(atom.terms[i]) == Term:
                    if atom.terms[i].isUnderscore():
                        canContinue = False
                if canContinue:
                    for ip in range(len(matchedVars)):
                        if type(matchedVars[ip]) == tuple:
                            if matchedVars[ip][0] == atom.terms[i]:
                                p = list(matchedVars[ip])
                                p[1] = symbLit.attributes[i]
                                p[2] = lit
                                matchedVars[ip] = tuple(p)

    started = False
    for builtVars in matchedVars:
        isConstant = type(builtVars) != tuple
        if started:
            results.write(", ")
            if isConstant or builtVars == matchedVars[-1]:
                results.write("and ")
        else:
            started = True
        if not isConstant:
            if foundLitNames.count(builtVars[2].literal.name) == 1:
                results.write(builtVars[0].name)
            else:
                results.write("the")
                results.write(" ")
                results.write(builtVars[1])

                results.write(" ")
                results.write(builtVars[0].name)

                results.write(" ")
                results.write("of the ")
                results.write(builtVars[2].literal.name)
                results.write(" ")
                results.write(get_literal_identifier(body, builtVars[2]))
        else:
            results.write(builtVars.name)
    return results.getvalue()


def generate_with(atom, symbol, builtinAtoms=None):
    if builtinAtoms is None:
        builtinAtoms = []
    results = StringIO()
    started = False
    for i in range(len(atom.terms)):
        canContinue = True
        if type(atom.terms[i]) == Term:
            if atom.terms[i].isUnderscore():
                canContinue = False
        if canContinue:
            if started:
                results.write(", ")
            else:
                started = True
            results.write("with")
            results.write(" ")
            results.write(symbol.attributes[i])
            results.write(" ")
            if type(atom.terms[i]) == Term:
                if atom.terms[i].isVariable():
                    foundMatchedBuiltin = False
                    userVariablesInBuiltin = []
                    for builtinAtom in builtinAtoms:
                        if not type(builtinAtom.terms[0]) == ArithmeticAtom:
                            if (builtinAtom.terms[0] == atom.terms[i]
                                    and builtinAtom.terms[0] not in userVariablesInBuiltin):
                                userVariablesInBuiltin.append(builtinAtom.terms[0])
                                foundMatchedBuiltin = True
                                results.write(atom.terms[i].name)
                                results.write(" ")
                                results.write(generate_compare_operator_sentence(builtinAtom.op))
                                results.write(" ")
                                results.write(builtinAtom.terms[1].toString())
                                builtinAtoms.remove(builtinAtom)
                    if not foundMatchedBuiltin:
                        results.write(atom.terms[i].name)

                else:
                    results.write("equal")
                    results.write(" ")
                    results.write("to")
                    results.write(" ")
                    results.write(atom.terms[i].name.strip('\"'))
            elif type(atom.terms[i]) == ArithmeticAtom:
                '''results.write("equal")   
                results.write(" ")
                results.write("to")   
                results.write(" ")'''
                results.write(atom.terms[i].toString())
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


def generate_relation(atom):
    # Eg. work_in("john",1).
    # --> Waiter John works in pub 1.
    # serve("john","alcoholic").
    # --> Waiter John serves a drink alcoholic.
    results = StringIO()
    atom_name = atom.name
    results.write(atom.terms[0].name.replace('"', ''))
    results.write(" ")
    results.write(atom_name)
    for i in range(len(atom.terms)):
        if i > 0:
            results.write(" ")
            results.write("and")
        results.write(" ")
        results.write(atom.terms[i].name.replace('"', ''))
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

    builtinAtoms = getBuiltinAtoms(rule)
    results.write(generate_body(rule, symbols, builtinAtoms))
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

    results.write(generateWhereForBuiltins(builtinAtoms))
    results.write(".")
    return results.getvalue()


def getBuiltinAtoms(rule):
    builtinAtoms = []
    for lit in rule.body.literals:
        if type(lit) == NafLiteral and type(lit.literal) == BuiltinAtom:
            builtinAtoms.append(lit.literal)
    return builtinAtoms


def generate_classical_statement(rule, symbols):
    # Eg. topmovie(X) :- movie(X,_,"spielberg",_).
    # -->
    # Whenever there is a movie with id X, with director equal to spielberg
    # then we must have a topmovie with id X.    
    results = StringIO()
    builtinAtoms = getBuiltinAtoms(rule)
    results.write(generate_body(rule, symbols, builtinAtoms))
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
    results.write(generateWhereForBuiltins(builtinAtoms))
    results.write(".")
    return results.getvalue()


def generate_strong_constraint(rule, symbols):
    # Eg. :- movie(X,_,_,1964), topmovie(Y), X = Y.
    # -->
    # It is prohibited that X is equal to Y, whenever there is a movie 
    # with id X, and with year equal to 1964, whenever there is a topMovie with id Y.
    results = StringIO()
    results.write("It is prohibited that")
    builtinAtoms = getBuiltinAtoms(rule)
    results.write(generate_body(rule, symbols, builtinAtoms, True))
    results.write(generateWhereForBuiltins(builtinAtoms))
    results.write(".")
    return results.getvalue()


def generate_weak_constraint(rule, symbols):
    results = StringIO()
    results.write("It is preferred")
    if type(rule.weight_at_level.beforeAt) != ArithmeticAtom:
        if rule.weight_at_level.beforeAt.name == "1":
            results.write(" as little as possible")

    if rule.weight_at_level.afterAt is not None:
        results.write(", ")
        results.write("with")
        results.write(" ")
        results.write("priority")
        results.write(" ")
        results.write(rule.weight_at_level.afterAt[0].name)
        results.write(",")
    results.write(" ")
    results.write("that")

    builtinAtoms = getBuiltinAtoms(rule)
    results.write(generate_body(rule, symbols, builtinAtoms, False, rule.weight_at_level.beforeAt))

    if type(rule.weight_at_level.beforeAt) != ArithmeticAtom:
        if rule.weight_at_level.beforeAt.isVariable():
            results.write("is")
            results.write(" ")
            if rule.weight_at_level.isMaximize:
                results.write("maximized")
            else:
                results.write("minimized")
    results.write(generateWhereForBuiltins(builtinAtoms))
    results.write(".")
    return results.getvalue()


def generate_head_choice(head, symbols):
    results = StringIO()
    atMost = False
    atLeast = False
    beetween = False
    exactly = False

    howMany = StringIO()

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
        howMany.write("exactly")
        howMany.write(" ")
        if head.lowerGuard is not None:
            howMany.write(head.lowerGuard.name)
        else:
            howMany.write(head.upperGuard.name)
    if atLeast:
        # at least 1 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        howMany.write("at least")
        howMany.write(" ")
        howMany.write(head.lowerGuard.name)
    if atMost:
        # at most 1 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        howMany.write("at most")
        howMany.write(" ")
        howMany.write(head.upperGuard.name)
    if beetween:
        # between 3 and 4 topmovie with id I such that there is a movie with director X, 
        #           and with id I.
        howMany.write("between")
        howMany.write(" ")
        howMany.write(head.lowerGuard.name)
        howMany.write(" ")
        howMany.write("and")
        howMany.write(" ")
        howMany.write(head.upperGuard.name)
    if head.lowerGuard is None and head.upperGuard is None:
        howMany.write("a")

    startedHeadElem = False
    for headElem in head.elements:
        if startedHeadElem:
            results.write(" ")
            results.write("or")
            # results.write(" ")
        else:
            startedHeadElem = True
            results.write(howMany.getvalue())
        results.write(" ")
        results.write(headElem.left_part.name)
        results.write(" ")
        results.write(generateWithInHead(symbols, headElem.left_part))
        if headElem.right_part is not None:
            results.write(" ")
            results.write("such that")
            results.write(" ")

            started = False
            for nafLit in headElem.right_part:
                # if type(nafLit.literal) != BuiltinAtom:
                if started:
                    results.write(",")
                    results.write(" ")
                symb = get_symbol(symbols, nafLit.literal)
                results.write(generate_there_is(nafLit, symb, {}, False, started))
                started = True

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

        results.write(generateWithInHead(symbols, atom))

    return results.getvalue()


def generateWhereForBuiltins(builtinAtoms):
    results = StringIO()
    if len(builtinAtoms) > 0:
        for builtinAtom in builtinAtoms:
            if type(builtinAtom.terms[0]) != ArithmeticAtom:
                results.write(", ")
                results.write("where")
                results.write(" ")
                results.write(builtinAtom.terms[0].toString())
                results.write(" ")
                results.write("is")
                results.write(" ")
                results.write(generate_compare_operator_sentence(builtinAtom.op))
                results.write(" ")
                results.write(builtinAtom.terms[1].toString())
    return results.getvalue()


def generateWithInHead(symbols, atom):
    results = StringIO()
    symbLit = get_symbol(symbols, atom)

    for i in range(len(symbLit.attributes)):
        if i > 0:
            results.write(",")
            results.write(" ")
        results.write("with")
        results.write(" ")
        results.write(symbLit.attributes[i])
        results.write(" ")

        if type(atom.terms[i]) == Term and not atom.terms[i].isVariable():
            results.write("equal")
            results.write(" ")
            results.write("to")
            results.write(" ")
        results.write(atom.terms[i].toString().strip('\"'))
    return results.getvalue()


def generate_body(rule, symbols, builtinAtoms, isStrongConstraint=False, costWeakTerm=None):
    body = rule.body
    results = StringIO()
    startedLits = False
    hasSumInBuiltin = False

    for builtinA in builtinAtoms:
        if type(builtinA.terms[0]) == ArithmeticAtom:
            hasSumInBuiltin = True

    if hasSumInBuiltin and isStrongConstraint:
        for builtinAtom in builtinAtoms:
            if type(builtinAtom.terms[0]) == ArithmeticAtom:
                if startedLits:
                    results.write(", whenever we have that")
                else:
                    startedLits = True
                results.write(" ")
                results.write(generate_operation_between(body, symbols, builtinAtom.terms[0]))
                results.write(generate_compare_of_arithmetic_builtin(builtinAtom.op, builtinAtom.terms[1]))

    tmpWheneverResults = None
    foundAggrs = []
    firstConstraintLiteralInSentence = None
    specialConstraintTranslationForLiteral = False

    foundLitNames = []
    for lit in body.literals:
        if type(lit) == NafLiteral and type(lit.literal) == ClassicalLiteral:
            foundLitNames.append(lit.literal.name)

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
                    if len(foundAggrs) > 0:
                        tmpWheneverResults.write(", ")
                        tmpWheneverResults.write("whenever")
                    elif costWeakTerm is not None:
                        if type(rule.weight_at_level.beforeAt) == ArithmeticAtom or rule.weight_at_level.beforeAt.isVariable():
                            tmpWheneverResults.write(" ")
                            tmpWheneverResults.write("whenever")
                    else:
                        tmpWheneverResults.write("Whenever")
                else:
                    if len(foundAggrs) > 0 or hasSumInBuiltin:
                        tmpWheneverResults.write(" ")
                        tmpWheneverResults.write("whenever")
                    else:
                        specialConstraintTranslationForLiteral = True
                startedLits = True
            symbLit = get_symbol(symbols, lit.literal)
            if not specialConstraintTranslationForLiteral:
                tmpWheneverResults.write(" ")
                literalVariable = None
                if type(costWeakTerm) == ArithmeticAtom:
                    if foundLitNames.count(lit.literal.name) > 1:
                        literalVariable = get_literal_identifier(body, lit)
                tmpWheneverResults.write(generate_there_is(lit, symbLit, builtinAtoms, literalVariable=literalVariable))
            else:
                specialConstraintTranslationForLiteral = False
                if not hasSumInBuiltin:
                    firstConstraintLiteralInSentence = " " + generate_there_is(lit, symbLit, builtinAtoms)
        elif type(lit) == AggregateLiteral:
            if not isStrongConstraint and costWeakTerm is None:
                if len(foundAggrs) > 0 or startedLits:
                    results.write(" ")
                    results.write("whenever")
                else:
                    results.write("Whenever")
                results.write(" ")
                results.write("we have that")
            else:
                if len(foundAggrs) > 0:
                    results.write(",")
                    results.write(" ")
                    results.write("whenever")
                    results.write(" ")
                    results.write("we have that")
            results.write(" ")
            results.write(generate_aggregate_subsentence(lit, symbols, costWeakTerm, isStrongConstraint))
            foundAggrs.append(lit)

    needVariable = False

    if len(foundAggrs) == 0:
        needVariable = True
    else:
        for foundAggr in foundAggrs:
            if (foundAggr.lowerOp == "=" and foundAggr.upperGuard is None) or (
                    foundAggr.upperOp == "=" and foundAggr.lowerGuard is None):
                if foundAggr.upperGuard is not None and foundAggr.upperGuard.isVariable():
                    needVariable = True
                elif foundAggr.lowerGuard is not None and foundAggr.lowerGuard.isVariable():
                    needVariable = True

    if tmpWheneverResults is not None:
        if costWeakTerm is not None and needVariable:

            if type(costWeakTerm) == ArithmeticAtom:
                results.write(" ")
                results.write(generate_operation_between(body, symbols, costWeakTerm))
                results.write(" ")
                results.write("is")
                results.write(" ")
                if rule.weight_at_level.isMaximize:
                    results.write("maximized")
                else:
                    results.write("minimized")
            else:
                if rule.weight_at_level.beforeAt.isVariable():
                    tmpWheneverResults.write(", ")
                    tmpWheneverResults.write(costWeakTerm.name)
                    tmpWheneverResults.write(" ")

        if firstConstraintLiteralInSentence is not None:
            if len(foundAggrs) > 0:
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
    elif aggregate.upperOp == ">" and aggregate.lowerGuard is None:
        operator = ">"
    elif aggregate.upperOp == ">=" and aggregate.lowerGuard is None:
        operator = ">="
    elif aggregate.upperOp == "<" and aggregate.lowerGuard is None:
        operator = "<"
    elif aggregate.upperOp == "<=" and aggregate.lowerGuard is None:
        operator = "<="
    elif aggregate.lowerOp == "<=" and aggregate.upperOp == "<=":
        operator = "between"
    elif ((aggregate.lowerOp == "!=" or aggregate.lowerOp == "<>") and aggregate.upperGuard is None
          or (aggregate.upperOp == "!=" or aggregate.upperOp == "<>") and aggregate.lowerGuard is None
          or (aggregate.lowerOp == "!=" or aggregate.lowerOp == "<>") and (
                  aggregate.upperOp == "!=" or aggregate.upperOp == "<>")):
        operator = "!="
    return operator


def generate_operation_between(body, symbols, arithAtom):
    results = StringIO()
    isSum = False
    isSub = False
    isMult = False
    isDiv = False
    if arithAtom.ops[0] == "+":
        isSum = True
    if arithAtom.ops[0] == "-":
        isSub = True
    if arithAtom.ops[0] == "*":
        isMult = True
    if arithAtom.ops[0] == "/":
        isDiv = True

    for op in arithAtom.ops:
        if op == "+":
            isSub = False
            isMult = False
            isDiv = False
        if op == "-":
            isSum = False
            isMult = False
            isDiv = False
        if op == "*":
            isSum = False
            isSub = False
            isDiv = False
        if op == "/":
            isSum = False
            isSub = False
            isMult = False
    isOp = isSum or isSub or isMult or isDiv

    if isOp:
        results.write("the")
        results.write(" ")

        if isSum:
            results.write("sum")
            results.write(" ")
        elif isSub:
            results.write("difference")
            results.write(" ")

        results.write("between")
        results.write(" ")

        results.write(generate_vars_symbols(body, symbols, arithAtom))

    return results.getvalue()


def generate_compare_of_arithmetic_builtin(op, compareTerm):
    results = StringIO()

    results.write(" ")
    results.write("is")
    results.write(" ")
    results.write(generate_compare_operator_sentence(op))
    results.write(" ")

    results.write(compareTerm.toString())

    return results.getvalue()


def generate_aggregate_subsentence(aggregate, symbols, costWeakTerm=None, isStrongConstraint=True):
    results = StringIO()
    # #AGGR{VL, X: scoreassignment(X,VL)} = 1
    # --->
    # the lowest value of a scoreAssignment with movie id X for each id is equal to 1        

    operator = None
    assignmentVar = None
    operator = getAggregateOperator(aggregate)
    if operator == "=":
        if (aggregate.lowerOp == "=" and aggregate.upperGuard is None) or (
                aggregate.upperOp == "=" and aggregate.lowerGuard is None):
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
    positionOfFoundVar = -1
    foundMultipleUseOfAggrTerm = False
    builtinAtoms = []
    removeAggrTerm = True

    # Search builtins
    for naf_literal in aggregate.aggregateElement[0].body.literals:
        if type(naf_literal) == NafLiteral and type(naf_literal.literal) == BuiltinAtom:
            builtinAtoms.append(naf_literal.literal)
            if naf_literal.literal.containsVar(aggrTerm):
                removeAggrTerm = False

    for naf_literal in aggregate.aggregateElement[0].body.literals:
        if type(naf_literal) == NafLiteral:
            if type(naf_literal.literal) == ClassicalLiteral:
                p = 0
                for t in naf_literal.literal.terms:
                    if t.name == aggrTerm.name:
                        if foundClassicalLiteral:
                            foundMultipleUseOfAggrTerm = True
                        else:
                            foundClassicalLiteral = naf_literal.literal
                            positionOfFoundVar = p
                    if t in forEachTerms:
                        subEach = StringIO()
                        subEach.write("for each")
                        subEach.write(" ")
                        symbLit = get_symbol(symbols, naf_literal.literal)
                        subEach.write(symbLit.attributes[p])
                        if forEachSubsentences[forEachTerms.index(t)] != None:
                            subEach.write(" ")
                            subEach.write(t.name)
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
        results.write(" ")
        symbLit = get_symbol(symbols, foundClassicalLiteral)
        results.write(symbLit.attributes[positionOfFoundVar])

        if foundMultipleUseOfAggrTerm:
            results.write(" ")
            results.write(aggrTerm.name)

        if forEachSubsentences is not None:
            for s in forEachSubsentences:
                if s is not None:
                    results.write(", ")
                    results.write(s)
                    results.write(",")

        if connective is not None:
            results.write(" ")
            results.write(connective)
        results.write(" ")
        results.write("a")
        results.write(" ")
        results.write(foundClassicalLiteral.name)
        results.write(" ")

        tmpLitTerm = None
        tmpSymbTerm = None
        if removeAggrTerm:
            tmpLitTerm = foundClassicalLiteral.terms.pop(positionOfFoundVar)
            tmpSymbTerm = symbLit.attributes.pop(positionOfFoundVar)
        results.write(generate_with(foundClassicalLiteral, symbLit, builtinAtoms))
        if removeAggrTerm:
            foundClassicalLiteral.terms.insert(positionOfFoundVar, tmpLitTerm)
            symbLit.attributes.insert(positionOfFoundVar, tmpSymbTerm)

        if len(aggregate.aggregateElement[0].body.literals) > 1:
            results.write(" ")
            startedIn = False
            for nafLit in aggregate.aggregateElement[0].body.literals:
                if nafLit.literal != foundClassicalLiteral:
                    if type(nafLit) == NafLiteral and type(nafLit.literal) == ClassicalLiteral:
                        if startedIn:
                            results.write(",")
                            results.write(" ")
                        else:
                            startedIn = True
                        results.write(nafLit.literal.name)
                        results.write(" ")
                        results.write(nafLit.literal.terms[0].name)
                        symbLit2 = get_symbol(symbols, nafLit.literal)
                        results.write(" ")
                        results.write(generate_with(nafLit.literal, symbLit2, builtinAtoms))
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
    results.write(generateWhereForBuiltins(builtinAtoms))
    return results.getvalue()

