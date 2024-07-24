node(Z) :- node(X), #count{Y: node(Y)} = Z.
:- hole(C), #count{C1: stitch(C,C1)} = N1, #count{C1: stitch(C1,C)} = N2, N1+N2>1.
:- hole(N1), #count{C1: stitch(C1,C)} = N2, N1+N2>1.
hole(N1+N2):- hole(N1), #count{C1: stitch(C1,C)} = N2, N1+N2>1.
hole(N1+N2):- hole(N1), hole(N2), 1=N1+N2.
:- 1=N1+N2,hole(N1), hole(N).
