#const timemax = 90.

isLinked(J1,J2) :- isLinked(J2,J1).

{changeAngle(J1,J2,A,AI,T) : joint(J1), joint(J2), J1>J2, angle(A), hasAngle(J1,AI,T), A<>AI, isLinked(J1,J2)} <= 1 :- time(T), T < timemax, T > 0.

:- changeAngle(J1,J2,A,AI,T), not ok(J1,J2,A,AI,T).

% affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=|(AC + (A-AP)) + 360|\\360, time(T).

hasAngle(J1,A,T+1) :- changeAngle(J1,_,A,_,T).

hasAngle(J1,A,T+1) :- affected(J1,A,_,T).

hasAngle(J1,A,T+1) :- hasAngle(J1,A,T), not changeAngle(J1,_,_,_,T), not affected(J1,_,_,T), T <= timemax.

:- goal(J,A), not hasAngle(J,A,timemax).
