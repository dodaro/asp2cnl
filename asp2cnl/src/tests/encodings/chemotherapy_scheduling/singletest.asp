%res(RID,DAY,TS..TS+PH4-1) :- x(RID,DAY,TS,PH4,_,_), PH4 > 0.

%res(RID,DAY,T) :- 10_min_ts(T), x(RID,DAY,TS,PH4,_,_), PH4 > 0, TS <= T, T < TS+PH4.

% numMin(DAY,T) :- T = #min{N: numbReg(DAY,N,_), N != 0}, day(DAY). 

:~ x(RID,DAY,_,_,_,"chair"), bed_with_registration_day_and_timeslot(ID,RID,DAY,_). [1@7,RID]