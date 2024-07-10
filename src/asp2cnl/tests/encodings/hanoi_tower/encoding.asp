% The meaning of the time predicate is self-evident. As for the disk
% predicate, there are k disks 1,2,...,k. Disks 1, 2, 3, 4 denote pegs. 
% Disks 5, ... are "movable". The larger the number of the disk, 
% the "smaller" it is.
%
% The program uses additional predicates:
% on(T,N,M), which is true iff at time T, disk M is on disk N
% move(t,N), which is true iff at time T, it is disk N that will be
% moved
% where(T,N), which is true iff at time T, the disk to be moved is moved
% on top of the disk N.
% goal, which is true iff the goal state is reached at time t
% steps(T), which is the number of time steps T, required to reach the goal (provided part of Input data)

% Read in data 
on(0,N1,N) :- on0(N,N1).
% The rule is used to configure the initial position of the disks.

onG(K,N1,N) :- ongoal(N,N1), step(K).
% The rule is used to define the goal of the problem.

% Specify valid arrangements of disks
% Basic condition. Smaller disks must be on larger ones
:- time(T), on(T,N1,N), N1>=N.
% The rule states that smaller disks must be on larger ones

% Specify a valid move (only for T< t)
 	% pick a disk to move
move(T,N) | nomove(T,N) :- disk(N), time(T), step(K), T< K.
% The rule selects a disk to move.

:- move(T,N1), move(T,N2), N1 != N2.
% The rule states that two different disk cannot be moved at the same step.

:- time(T), step(K), T< K, not diskmoved(T).
% The rule ensures that for each step there must be a disk moved.

diskmoved(T) :- move(T,FV).
% The rules states that a disk that is moved is a disk moved.

% pick a disk onto which to move
dwhere(T,N) | noWhere(T,N) :- disk(N), time(T), step(K), T< K.
% The rule guesses the disks to be moved at a certain time.

:- dwhere(T,N1), dwhere(T,N2), N1 != N2.
% The rule ensures that only one disk can be moved at a certain time.

:- time(T), step(K), T< K, not diskWhere(T).
diskWhere(T) :- dwhere(T,FV).
% The rules ensure that at every time a disk must be moved


% pegs cannot be moved
:- move(T,N), N < 5.
% The rule ensures that pegs are not moved.

% only top disk can be moved
:- on(T,N,N1), move(T,N).
% The rule ensures that only top disk are moved.

% a disk can be placed on top only.
:- on(T,N,N1), dwhere(T,N).
% The rule states that a disk can be placed on top only.

% no disk is moved in two consecutive moves
:- move(T,N), move(TM1,N), TM1=T-1.
% The rule states that a disk cannot be moved for two consecutive moves.

% Specify effects of a move
on(TP1,N1,N) :- move(T,N), dwhere(T,N1), TP1=T+1.
on(TP1,N,N1) :- time(T), step(K), T< K, on(T,N,N1), not move(T,N1), TP1=T+1.
% The rules are used to update the disk position for the next step. 

% Goal description
:- not on(K,N,N1), onG(K,N,N1), step(K).
:- on(K,N,N1), not onG(K,N,N1), step(K).
% The rules ensure that the goal of the problem is achieved.

% Solution
	put(T,M,N) :- move(T,N), dwhere(T,M), step(K), T< K.
% (questa regola non serve?)

% BUGS 
% Fv e Fv1, 
% steps lo vede come step
% where errore di parsing
