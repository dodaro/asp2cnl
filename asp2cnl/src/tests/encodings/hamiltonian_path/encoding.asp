connected_to(1,X) :- node(1), node(X), X = 2.
connected_to(1,X) :- node(1), node(X), X = 3.
connected_to(2,X) :- node(2), node(X), X = 1.
connected_to(2,X) :- node(2), node(X), X = 4.
connected_to(3,X) :- node(3), node(X), X = 1.
connected_to(3,X) :- node(3), node(X), X = 4.
connected_to(4,X) :- node(4), node(X), X = 3.
connected_to(4,X) :- node(4), node(X), X = 5.
connected_to(5,X) :- node(5), node(X), X = 3.
connected_to(5,X) :- node(5), node(X), X = 4.
{path_to(X,Y): node(Y), connected_to(Y,X)} :- node(X).
:- node(X), #count{Y: path_to(X,Y), node(Y)} != 1.
:- node(Y), #count{X: path_to(X,Y), node(X)} != 1.
reachable(start) :- node(start).
reachable(Y) :- reachable(X), node(X), path_to(X,Y), node(Y).
:- node(RCHBL_D), not reachable(RCHBL_D).
