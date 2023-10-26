%working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

%%% topmovie(X) :- movie(X,_,"spielberg",_).

movie(X,"jurassicPark",spielberg,Y) :- topmovie(X), director(ciccio). 

%---> Whenever there is a movie with director equal to spielberg, 
%     and with id X, whenever there is ____, then we must have a topmovie with id X, with name Y
%     then 

% a (X) :- b(X), c(Y).

%%% topmovie(ciccio) :- movie(X,_,"spielberg",_).
