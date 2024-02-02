{x(RID,DAY,TS,PH4,0,S) : 10_min_ts(TS), day(DAY)} = 1 :- registration(RID,0,_,PH4,PH3,PH2,PH1,S).

{x(RID,DAY+DAY2,TS,PH4,ORDER,S) : 10_min_ts(TS)} = 1 :- x(RID,DAY,_,_,N,_), ORDER=N+1, day(DAY+DAY2),registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S).

:- x(RID,DAY,TS,PH4,_,_), PH4 > 50, TS < 24.

:- x(RID,DAY,TS,_,ORDER,_), registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S), TS-PH3-PH2-PH1<1.

1 <= {bed(ID,RID,DAY) : bed(ID); chair(ID,RID,DAY) : chair(ID)} <= 1:- x(RID,DAY,_,_,_,_).

%res(RID,DAY,TS..TS+PH4-1) :- x(RID,DAY,TS,PH4,_,_), PH4 > 0. 
%%chair(ID,RID,DAY,TS) :- chair(ID,RID,DAY), res(RID,DAY,TS). 
%%bed(ID,RID,DAY,TS) :- bed(ID,RID,DAY), res(RID,DAY,TS). 
%%:- #count{RID: chair(ID,RID,DAY,TS)} > 1, day(DAY), ts(TS), chair(ID). 
%%:- #count{RID: bed(ID,RID,DAY,TS)} > 1, day(DAY), ts(TS), bed(ID).

%%support(RID,DAY,TS) :- x(RID,DAY,PH4,_,_,_), registration(RID,ORDER,_,_,PH3,PH2,_,_), PH2 > 0, TS=PH4-PH3-PH2, day(DAY), 5_min_ts(TS).
