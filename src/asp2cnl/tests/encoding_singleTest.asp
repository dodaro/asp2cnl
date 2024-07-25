% affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=(A-AP+B), time(T).
% affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=C + (A-AP) - (E * (F + KL) ), time(T).
% affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=(AC + (A-AP)) + 360, time(T).
affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=|(AC + (A-AP)) + 360|, time(T).

% affected(J1,AN,AC,T) :- changeAngle(J2,_,A,AP,T), hasAngle(J1,AC,T),J1>J2, angle(AN), AN=|(AC + (A-AP)) + 360|\\360, time(T).
