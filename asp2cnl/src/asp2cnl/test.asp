#const granularity = 90.
{pathto(X,Y): node(Y), connectedto(Y,X)} :- node(X).
:- node(X), #count{Y: pathto(X, Y), node(T)} != 1 .