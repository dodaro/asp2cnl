{x(RID,DAY,TS,PH4,0,S) : 10_minutes_timeslot(TS), day(DAY)} = 1 :- registration(RID,0,_,PH4,PH3,PH2,PH1,S).

{x(RID,DAY+DAY2,TS,PH4,ORDER,S) : 10_minutes_timeslot(TS)} = 1 :- x(RID,DAY,_,_,N,_), ORDER=N+1, day(DAY+DAY2),registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S).

:- x(RID,DAY,TS,PH4,_,_), PH4 > 50, TS < 24.
:- x(RID,DAY,TS,_,ORDER,_), registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S), TS-PH3-PH2-PH1<1.

1 <= {bed_with_registration_and_day(ID,RID,DAY) : bed(ID); chair_with_registration_and_day(ID,RID,DAY) : chair(ID)} <= 1 :- x(RID,DAY,_,_,_,_).

%% res(RID,DAY,TS..TS+PH4-1) :- x(RID,DAY,TS,PH4,_,_), PH4 > 0. 
res(RID,DAY,T) :- 10_minutes_timeslot(T), x(RID,DAY,TS,PH4,_,_), PH4 > 0, TS <= T, T < TS+PH4.
chair_with_registration_day_and_timeslot(ID,RID,DAY,TS) :- chair_with_registration_and_day(ID,RID,DAY), res(RID,DAY,TS). 
bed_with_registration_day_and_timeslot(ID,RID,DAY,TS) :- bed_with_registration_and_day(ID,RID,DAY), res(RID,DAY,TS). 
:- #count{RID: chair_with_registration_day_and_timeslot(ID,RID,DAY,TS)} > 1, day(DAY), 10_minutes_timeslot(TS), chair(ID). 
:- #count{RID: bed_with_registration_day_and_timeslot(ID,RID,DAY,TS)} > 1, day(DAY), 10_minutes_timeslot(TS), bed(ID).

support(RID,DAY,TS) :- x(RID,DAY,PH4,_,_,_), registration(RID,ORDER,_,_,PH3,PH2,_,_), PH2 > 0, TS=PH4-PH3-PH2, day(DAY), 5_minutes_timeslot(TS).

numbReg(DAY,N,TS) :- N = #count{RID: support(RID,DAY,TS)}, day(DAY), 5_minutes_timeslot(TS).
numMax(DAY,T) :- T = #max{N: numbReg(DAY,N,_)}, day(DAY).
numMin(DAY,T) :- T = #min{N: numbReg(DAY,N,_), N != 0}, day(DAY). 

numbDay(DAY,N) :- N = #count{RID: support(RID,DAY,_)}, day(DAY).
numMaxDay(T) :- T = #max{N: numbDay(DAY, N)}.

:~ x(RID,DAY,_,_,_,"chair"), bed_with_registration_day_and_timeslot(ID,RID,DAY,_). [1@7,RID]
:~ x(RID,DAY,_,_,_,"bed"), chair_with_registration_day_and_timeslot(ID,RID,DAY,_). [1@7,RID]

:~ numMax(DAY,T). [T@6, DAY]
:~ numMax(DAY,MAX), numMin(DAY,MIN). [MAX-MIN@5,DAY]
:~ numMaxDay(N). [N@4]


