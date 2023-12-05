{chosen(ND_D)} :- node(ND_D).
:- not connectedto(X,Y), node(X), chosen(X), node(Y), chosen(Y), X != Y.
:~ #count{D: chosen(D)} = X_ABD45092_8384_4F3A_A91D_7642B8666A29. [-X_ABD45092_8384_4F3A_A91D_7642B8666A29@3]
