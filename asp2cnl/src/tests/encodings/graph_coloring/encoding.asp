node(1).
node(2).
node(3).
color("red").
color("green").
color("blue").
connected_to(1,X) :- node(1), node(X), X = 2.
connected_to(1,X) :- node(1), node(X), X = 3.
connected_to(2,X) :- node(2), node(X), X = 1.
connected_to(2,X) :- node(2), node(X), X = 3.
connected_to(3,X) :- node(3), node(X), X = 1.
connected_to(3,X) :- node(3), node(X), X = 2.


1 <= {assigned_to(ND_D,CLR_D): color(CLR_D)} <= 1 :- node(ND_D).
:- connected_to(X,Y), node(X), assigned_to(X,C), node(Y), assigned_to(Y,C), color(C).
