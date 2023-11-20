
% director("alice") :- #min{VL: scoreassignment(X,VL)} = 1.

% :- topmovie(X), #max{VL: scoreassignment(X,VL)} = 1.
% :- topmovie(X), #count{VL: scoreassignment(X,VL)} = 1.
:- topmovie(X), #sum{VL: scoreassignment(X,VL)} = 1.

