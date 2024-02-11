{x(RID,DAY,TS,PH4,0,S) : 10_min_ts(TS), day(DAY)} = 1 :- registration(RID,0,_,PH4,PH3,PH2,PH1,S).

{x(RID,DAY+DAY2,TS,PH4,ORDER,S) : 10_min_ts(TS)} = 1 :- x(RID,DAY,_,_,N,_), ORDER=N+1, day(DAY+DAY2),registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S).

:- x(RID,DAY,TS,PH4,_,_), PH4 > 50, TS < 24.
:- x(RID,DAY,TS,_,ORDER,_), registration(RID,ORDER,DAY2,PH4,PH3,PH2,PH1,S), TS-PH3-PH2-PH1<1.

1 <= {bed3(ID,RID,DAY) : bed(ID); chair3(ID,RID,DAY) : chair(ID)} <= 1 :- x(RID,DAY,_,_,_,_).

%% res(RID,DAY,TS..TS+PH4-1) :- x(RID,DAY,TS,PH4,_,_), PH4 > 0. 
res(RID,DAY,T) :- 10_min_ts(T), x(RID,DAY,TS,PH4,_,_), PH4 > 0, TS <= T, T < TS+PH4.

chair4(ID,RID,DAY,TS) :- chair3(ID,RID,DAY), res(RID,DAY,TS). 
bed4(ID,RID,DAY,TS) :- bed3(ID,RID,DAY), res(RID,DAY,TS). 
:- #count{RID: chair4(ID,RID,DAY,TS)} > 1, day(DAY), 10_min_ts(TS), chair(ID). 
:- #count{RID: bed4(ID,RID,DAY,TS)} > 1, day(DAY), 10_min_ts(TS), bed(ID).

support(RID,DAY,TS) :- x(RID,DAY,PH4,_,_,_), registration(RID,ORDER,_,_,PH3,PH2,_,_), PH2 > 0, TS=PH4-PH3-PH2, day(DAY), 5_min_ts(TS).

numbReg(DAY,N,TS) :- N = #count{RID: support(RID,DAY,TS)}, day(DAY), 5_min_ts(TS).
numMax(DAY,T) :- T = #max{N: numbReg(DAY,N,_)}, day(DAY).
numMin(DAY,T) :- T = #min{N: numbReg(DAY,N,_), N != 0}, day(DAY). 

numbDay(DAY,N) :- N = #count{RID: support(RID,DAY,_)}, day(DAY).
numMaxDay(T) :- T = #max{N: numbDay(DAY, N)}.

:~ x(RID,DAY,_,_,_,"chair"), bed4(ID,RID,DAY,_). [1@7,RID]
:~ x(RID,DAY,_,_,_,"bed"), chair4(ID,RID,DAY,_). [1@7,RID]

:~ numMax(DAY,T). [T@6, DAY]
:~ numMax(DAY,MAX), numMin(DAY,MIN). [MAX-MIN@5,DAY]
:~ numMaxDay(N). [N@4]

%%% {nurses3(ID,RID,DAY) : nurse(ID)} = 1 :- x(RID,DAY,_,_,_,_).

%%% nurses4(ID,RID,DAY,TS) :- nurses3(ID,RID,DAY), res(RID,DAY,TS).
%%% :- #count{RID: nurses4(ID,RID,DAY,TS)} > K, day(DAY), 10_min_ts(TS), nurse(ID), nurseLimits(K).

%%% %% :- drug(DRUG,LMT,DAY), #count{RID: x(RID,DAY,_,_,ORDER,_), registration10(RID,_,ORDER,_,_,_,_,_,_,DRUG)} > LMT.

%%% %% :- x(RID,DAY,36,_,PH4,_,_).

%%% :~ registration10(RID,0,_,_,_,_,_,_,1,_), x(RID,_,TS,_,_,_). [TS@3,RID]

%%% :~ registration10(RID,0,_,_,_,_,_,_,2,_), x(RID,_,TS,_,_,_). [TS@3,RID]

%%% :~ registration10(RID,0,_,_,_,_,_,_,3,_), x(RID,_,TS,_,_,_). [TS@3,RID]
