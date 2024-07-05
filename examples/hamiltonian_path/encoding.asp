node(1).
node(2).
node(3).
node(4).
node(5).
% The rules define the nodes.

connected_to(1,2).
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
% The rule defines the connection between the nodes.


{path_to(X,Y): node(Y), connected_to(Y,X)} :- node(X).
% The rule is used to select a connection between two nodes as a path to the two nodes.


:- node(X), #count{Y: path_to(X,Y), node(Y)} != 1.
:- node(Y), #count{X: path_to(X,Y), node(X)} != 1.
% The rules are used to ensure that a node has just one path to another node.


reachable(start) :- node(start).
% The rule state that node start is reachable.

reachable(Y) :- reachable(X), node(X), path_to(X,Y), node(Y).
% The rule defines that a node is reachable is there is a path to that node from another reachable node.

:- node(RCHBL_D), not reachable(RCHBL_D).
% The rule ensures that there are not nodes not reachable.
