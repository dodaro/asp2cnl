%#const granularity = 90.
%#const timemax = 90.
link(J2,J1) :- link(J1,J2).
{rotation(J1,J2,A,AI,T): joint(J1), joint(J2), angle(A), link(J1,J2), position(J1,AI,T)} <= 1 :- T > 0, time(T).
:- T >= timemax, rotation(_,_,_,_,T).
:- J1 <= J2, rotation(J1,J2,_,_,_).
:- (A)/360 = (AI)/360, rotation(_,_,A,AI,_).
:- (A + granularity)/360 != (AI)/360, rotation(_,_,A,AI,_), (A)/360 > (0)/360, (AI)/360 > (A)/360.
:- (AI + granularity)/360 != (A)/360, rotation(_,_,A,AI,_), (A)/360 > (AI)/360, (AI)/360 > (0)/360.
:- (360 - granularity)/360 != (A)/360, rotation(_,_,A,0,_).
:- (360 - granularity)/360 != (AI)/360, rotation(_,_,A,AI,_), (A)/360 = (0)/360.
1 <= {position(J,A,T): angle(A)} <= 1 :- joint(J), time(T).
:- (A1)/360 != (A2)/360, position(J,A1,T), position(J,A2,T+1), not rotation(_,_,_,_,T), T <= timemax.
:- (A1)/360 != (A2)/360, position(J1,A1,T), rotation(J1,_,A2,_,T-1).
:- (AN)/360 != (|AC+(A-AP)+360|)/360, time(T), position(J1,AN,T+1), rotation(J2,_,A,AP,T), position(J1,AC,T), J1 > J2.
:- (A1)/360 != (A2)/360, position(J1,A1,T), position(J1,A2,T+1), rotation(J2,_,_,_,T), J2 > J1, T <= timemax.
:- (A1)/360 != (A2)/360, goal(J,A1), position(J,A2,timemax).