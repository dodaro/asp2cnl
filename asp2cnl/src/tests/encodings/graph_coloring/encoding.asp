node(1).
node(2).
node(3).
% The rules defines the nodes.

color("red").
color("green").
color("blue").
% The rule defines the colors.

connected_to(1,X) :- node(1), node(X), X = 2.
connected_to(1,X) :- node(1), node(X), X = 3.
connected_to(2,X) :- node(2), node(X), X = 1.
connected_to(2,X) :- node(2), node(X), X = 3.
connected_to(3,X) :- node(3), node(X), X = 1.
connected_to(3,X) :- node(3), node(X), X = 2.
% The rule defines the connection between the nodes.

1 <= {assigned_to(ND_D,CLR_D): color(CLR_D)} <= 1 :- node(ND_D).
% The rule is used to assign a color to each node.

:- connected_to(X,Y), node(X), assigned_to(X,C), node(Y), assigned_to(Y,C), color(C).
% The rule ensures that the same color is not assigned to two different connected nodes.
