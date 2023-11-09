%% serve non ha schemi. Ignoro la regola?
% working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

topmovie(X) :- movie(X,_,"spielberg",1990).

% Buggy
movie(X,"jurassicPark",spielberg,Y) :- Y != 5, topmovie(X), not director(Y). 

% Ok
%Possible versions?
% 1 - Whenever there is a topmovie with id X, whenever there is  
%    a director with name Y then we must have a movie with id X, 
%    with title equal to "jurassicPark", with director Y.
% --
% 2 - Whenever there is a topmovie with id X, whenever there is not 
%    a director with name Y different from 5 then we must have a movie with id X, 
%    with title equal to "jurassicPark", with director equal to spielberg, with year Y.

movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y != 5. 
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y <> 5.
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y < 5.
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y <= 5.
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y = 5.
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y > 5.
movie(X,"jurassicPark", spielberg,Y) :- topmovie(X), not director(Y), Y >= 5.

% Whenever there is a topmovie with id different from Y, whenever there is not 
% a director with name Y then we must have a movie with id X, with title equal to 
% "jurassicPark", with director equal to spielberg, with year Y.

movie(X,"jurassicPark",spielberg,Y) :- X = Y, topmovie(X), not director(Y). 
movie(X,"jurassicPark",spielberg,Y) :- topmovie(X), X = Y, not director(Y). 

% <> != different from
% <     less than
% <=    less than or equal to
% =     equal to
% >     greater than
% >=    greater than or equal to 
