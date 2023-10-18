from io import StringIO

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
        atom = rule.head[0].atoms[0]       
        symb = get_symbol(symbols, atom.name)     
        if len(atom.terms) == 1:
            if symb is None:
                results.write(generate_is_a(atom))            
            else:
                print(symb)
                results.write(generate_there_is(atom, symb))            
            results.write("\n")                                                   

        elif len(atom.terms) >= 2:  
            
            if symb is not None:
                results.write(generate_there_is(atom, symb))   
            else:
                print("NONE Symbol for " + atom.name)
            results.write("\n")           
                #if "_" in atom.name:                               
                    #Eg. work_in("john",1). --> Waiter John works in pub 1.
            '''
            symb = get_symbol(symbols, atom.name.replace("_", " "))
            results.write(symb.attributes[0].replace('"', '').capitalize())
            results.write(" ")
            results.write(atom.terms[0].replace('"', '').capitalize())
            results.write(" ")
            results.write(symb.predicate)
            results.write(" ")
            results.write(atom.terms[1].replace('"', ''))
            results.write(".")

            results.write("\n")
            '''
    return results.getvalue()

def generate_is_a(atom):
    #Eg. pub(1). --> 1 is a pub.
    results = StringIO()    
    results.write(atom.terms[0].replace('"', '').capitalize()) 
    results.write(" ")
    results.write("is a") 
    results.write(" ")
    results.write(atom.name)                 
    results.write(".") 
    return results.getvalue()

def generate_there_is(atom, symbol):
    #Eg. movie(1,"jurassicPark","spielberg",1993).
    # -->
    #There is a movie with id equal to 1, with director equal to spielberg, with title equal to jurassicPark, with year equal to 1993.
    results = StringIO()
    results.write("There is a") 
    results.write(" ")
    results.write(atom.name)
    results.write(" ")
    started = False
     
    for i in range(len(atom.terms)):
        if started:
            results.write(", ")
        else:
            started = True    
        results.write("with")
        results.write(" ")                        
        results.write(symbol.attributes[i])
        results.write(" ")   
        results.write("equal to")
        results.write(" ")
        results.write(atom.terms[i])
    results.write(".")
    return results.getvalue()
