% a(1).
% a (X) :- b(X), not c(Y, Z).
% working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

% topmovie(X) :- movie(X,_,"spielberg",_).

% a(X, Y, Z) :- c(X, K), Y = 1, Z != 2.

% scoreassignment(I,1) | scoreassignment(I,2) | scoreassignment(I,3) :- movie(I,_,_,_).
0 <= {topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_)} <= 1 :- director(X), X != spielberg.



