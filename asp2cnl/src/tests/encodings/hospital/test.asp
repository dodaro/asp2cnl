% {x(RID,DAY,TS,PH4,0,S) : timeslot(TS), day(DAY)} = 1 :- registration(RID,0,_,PH4,PH3,PH2,PH1,S).

{x(RID,DAY+DAY2,TS,PH4,ORDER,S) : timeslot(TS)} = 1 :- x(RID,DAY,_,_,N,_), ORDER=N+1, day(DAY+DAY2),registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S).