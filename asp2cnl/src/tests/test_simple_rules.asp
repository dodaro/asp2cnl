%working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

%%% topmovie(X) :- movie(X,_,"spielberg",1990).

movie(X,"jurassicPark",spielberg,Y) :- Y <> 5, topmovie(X), not director(Y). 

% a (X) :- b(X), c(Y).

%%% topmovie(ciccio) :- movie(X,_,"spielberg",_).
