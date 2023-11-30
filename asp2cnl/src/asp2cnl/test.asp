% a(1).
% a (X) :- b(X), not c(Y, Z).
% working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

% topmovie(X) :- movie(X,_,"spielberg",_).

% a(X, Y, Z) :- c(X, K), Y = 1, Z != 2.

% scoreassignment(I,1) | scoreassignment(I,2) | scoreassignment(I,3) :- movie(I,_,_,_), movie2(I2,_,_,_), not movie3(I3,_,_,_).
% 0 <= {topmovie(I)} <= 1 :- director(X), X != spielberg.
% 0 <= {topmovie(I): not movie(I,_,X,_)} <= 1 :- director(X), X != spielberg.

% 0 <= {topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_)} >= 1 :- director(X), X != spielberg.
% {topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_); topmovie(I):movie(I,_,X,_)} >= 1 :- director(X), X != spielberg.



%a(1) :- scoreassignment(X,K), 1 < #min{VL,G: scoreassignment(X,VL), ciccio(X);VL2,G2: scoreassignment(X2,VL2), ciccio(X2)} > 2.
%a(1) :- 1 < #min{VL,G: scoreassignment(X,VL), ciccio(X);VL2,G2: scoreassignment(X2,VL2), ciccio(X2)} > 2, scoreassignment(X,K).

%:- topmovie(I), scoreassignment(I,V). 
:~ topmovie(I), scoreassignment(I,V). [-V@2,I,V]

