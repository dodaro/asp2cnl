{chosen(ND_D)} :- node(ND_D).
:- not connected_to(X,Y), node(X), chosen(X), node(Y), chosen(Y), X != Y.
:~ #count{D: chosen(D)} = X. [-X@3]
