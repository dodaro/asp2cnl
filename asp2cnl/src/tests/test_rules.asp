waiter("john").
pub(1).
patron("alice").
% movie(1,"jurassicPark","spielberg",1993).
% scoreassignment(1, 30).
.\te
%% serve non ha schemi. Ignoro la regola?
% working(W) :- serve(W, X_574408ca_c2cd_43b2_a68a_0eae7285f99d).

topmovie(X) :- movie(X,_,"spielberg",1990).

movie(X,"jurassicPark",spielberg,Y) :- Y != 5, topmovie(X), not director(Y). 


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

:- movie(X,_,_,1964), topmovie(Y), topmovie(Z).
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

:- topmovie(X), #min{VL: scoreassignment(X,VL)} = 1.
% --->
% It is prohibited that the lowest value of a scoreassignment with id X is equal to 1 
% whenever there is a topmovie with id X.

:- #min{VL: scoreassignment(X,VL)} = 1, topmovie(X), scoreassignment(X,K).
% --->
% It is prohibited that the lowest value of a scoreassignment with id X is equal to 1 
% whenever there is not a topmovie with id X, whenever there is a scoreassignment with id X, with value K.

:- not topmovie(X), #min{VL: scoreassignment(X,VL)} = 1, scoreassignment(X,K).
% --->
% It is prohibited that the lowest value of a scoreassignment with id X is equal to 1 
%       whenever there is not a topmovie with id X, whenever there is a scoreassignment with id X, with value K.

:- topmovie(X), #sum{VL: scoreassignment(X,VL)} = 1.
:- topmovie(X), 1 <= #sum{VL: scoreassignment(X,VL)} <= 1.
:- topmovie(X), 1 >= #sum{VL: scoreassignment(X,VL)} >= 1.
:- topmovie(X), 1 = #sum{VL: scoreassignment(X,VL)}.
:- topmovie(X), 1 = #sum{VL: scoreassignment(X,VL)} = 1.
% --->
% It is prohibited that the total value of a scoreassignment with id X 
%       is equal to 1 whenever there is a topmovie with id X.

:- topmovie(X), #sum{VL: scoreassignment(X,VL)} > 1.
% --->
% It is prohibited that the total value of a scoreassignment with id X 
% is greater than 1 whenever there is a topmovie with id X

:- topmovie(X), #sum{VL: scoreassignment(X,VL)} >= 1.
% --->
% It is prohibited that the total value of a scoreassignment with id X 
% is greater than or equal to 1 whenever there is a topmovie with id X

:- topmovie(X), #sum{VL: scoreassignment(X,VL)} < 1.
% --->
% It is prohibited that the total value of a scoreassignment with id X 
% is less than 1 whenever there is a topmovie with id X

:- topmovie(X), #sum{VL: scoreassignment(X,VL)} <= 1.
% --->
% It is prohibited that the total value of a scoreassignment with id X 
% is less than or equal to 1 whenever there is a topmovie with id X

% DOMANDE
% director("alice") :- #min{VL: scoreassignment(X,VL)} = 1.
% :- topmovie(X), 1 <= #sum{VL: scoreassignment(X,VL)} <= 2.
% :- topmovie(X), 1 <= #sum{VL,A,B: scoreassignment(X,VL), movie(X)} <= 2.

:- #sum{VL,X: scoreassignment(X,VL)} <= 2.

% DOMANDE 2
%% CASO 1
%% RULE
:- topmovie(1), #sum{VLL, X: scoreassignment(X, VLL), topmovie(X)} <= 2 .
%% 
%% TRANSLATED IN:
%% It is prohibited that the total of value, for each id, that have a scoreassignment topmovie X is less than 
%% or equal to 2 whenever 
%% there is a topmovie with id equal to 1.
%% 
%% TRANSLATION BACK:
:- #sum{VL,X: scoreassignment(X,VL), topmovie(X)} <= 2, topmovie(1).
%%
%% CASO 2
%% RULE:
%% :- topmovie(1), #sum{VLL, X: scoreassignment(X, VLL), topmovie(X)} <= 2 .
%%
%% TRANSLATED IN:
%% It is prohibited that the total of value, for each id, that have a scoreassignment with id X topmovie X 
%% is less than or equal to 2 whenever there is a topmovie with id equal to 1.
%%
%% TRANSLATION BACK:
%%
% VERBI? ATOMO work_in

:~ topmovie(I), scoreassignment(I,V). [V@2,I,V]

:~ #sum{VL: scoreassignment(_,VL)} = X. [X@2]

:~ #sum{VL: scoreassignment(_,VL)} = X, topmovie(Y). [Y@2]

topmovie(K) :- #sum{VL: scoreassignment(X,VL)} <= 2, topmovie(K).

topmovie(K) :- 1 <= #sum{VL: scoreassignment(X,VL)} <= 2, topmovie(K).

:~ #sum{VL: scoreassignment(_, VL)} = X , topmovie(Y). [-Y@2]


{topmovie(I):movie(I,_,X,_), waiter(X)} = 1 :- director(X), X != spielberg.

%%%% {topmovie(I):movie(I,_,X,_), not waiter(X)} = 1 :- director(X), X != spielberg.

topmovie(K) :- 1 <= #sum{VL: scoreassignment(X,VL), waiter(VL)} <= 2, topmovie(K).

{topmovie(I)} :- movie(I,_,X,_).

:- #count{X, I: scoreassignment(X, Y), movie(I,_,_,_), topmovie(X), not topmovie(I)} = Z, #count{X, Y: scoreassignment(X, Y)} = K.






