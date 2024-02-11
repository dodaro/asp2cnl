%res(RID,DAY,TS..TS+PH4-1) :- x(RID,DAY,TS,PH4,_,_), PH4 > 0.

res(RID,DAY,T) :- 10_min_ts(T), x(RID,DAY,TS,PH4,_,_), PH4 > 0, TS <= T, T < TS+PH4.


