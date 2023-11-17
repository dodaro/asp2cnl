waiter("john").
pub(1).
patron("alice").
% movie(1,"jurassicPark","spielberg",1993).
% scoreassignment(1, 30).

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

:- movie(X,_,_,1964), topmovie(Y).
%% :- movie(X,_,_,1964), topmovie(Y), X = Y.
%% :- movie(X,_,_,1964), topmovie(Y), X != Y.

scoreassignment(I,1) | scoreassignment(I,2) | scoreassignment(I,3) :- movie(I,_,_,_).


{topmovie(I):movie(I,_,X,_)} <= 1 :- director(X), X != spielberg.
% ----> at most
% Whenever there is a director with name X different from spielberg 
%         then we can have at most 1 topmovie with id I such that there is a movie with director X, 
%           and with id I.

1 <= {topmovie(I):movie(I,_,X,_)} :- director(X), X != spielberg.
% ----> at least
% Whenever there is a director with name X different from spielberg 
%         then we can have at least 1 topmovie with id I such that there is a movie with director X, 
%           and with id I.


2 <= {topmovie(I):movie(I,_,X,_)} <= 3 :- director(X), X != spielberg.
% ----> between
% Whenever there is a director with name X different from spielberg then we can have between 2 
% and 3 topmovie with id I such that there 
% is a movie with id I, with director X.

1 <= {topmovie(I):movie(I,_,X,_)} <= 1 :- director(X), X != spielberg.
1 = {topmovie(I):movie(I,_,X,_)}  :- director(X), X != spielberg.
{topmovie(I):movie(I,_,X,_)} = 1 :- director(X), X != spielberg.
% ----> exactly
% Whenever there is a director with name X different from spielberg then we can have exactly 1 topmovie 
% with id I such that there is a movie with id I, with director X.

% <> != different from
% <     less than
% <=    less than or equal to
% =     equal to
% >     greater than
% >=    greater than or equal to 
