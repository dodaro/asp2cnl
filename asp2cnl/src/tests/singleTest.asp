timeslot(0,"07:30 AM").
1 <= {assignment_to(DY_DY,RGSTRTN_D,0,TMSLT_TMSLT): day(DY_DY,_), timeslot(TMSLT_TMSLT,_)} <= 1 :- registration(RGSTRTN_D,0,_,_,_,_,_).
%1 <= {assignment_to(D+W,P,OR,TMSLT_TMSLT): timeslot(TMSLT_TMSLT,_)} <= 1 :- registration(P,OR,W,_,_,_,_), assignment(P,OR-1,D,_), day(D+W,_).
%:- registration(_,_,_,RGSTRTN_DRTN_F_TH_FRST_PHS,RGSTRTN_DRTN_F_TH_SCND_PHS,RGSTRTN_DRTN_F_TH_THRD_PHS,_), assignment(_,_,_,T), RGSTRTN_DRTN_F_TH_FRST_PHS + RGSTRTN_DRTN_F_TH_SCND_PHS + RGSTRTN_DRTN_F_TH_THRD_PHS <= T, registration(RGSTRTN_D,RGSTRTN_RDR,_,RGSTRTN_DRTN_F_TH_FRST_PHS,RGSTRTN_DRTN_F_TH_SCND_PHS,RGSTRTN_DRTN_F_TH_THRD_PHS,_), assignment(RGSTRTN_D,RGSTRTN_RDR,_,T).
%1 <= {x_e5ad5465_7192_45a1_9799_2256b9e658ec(D,S,P,SSGNMNT_RDR,T): seat(S,_)} <= 1 :- patient(P,_), assignment(P,SSGNMNT_RDR,D,T), PH4 > 0, registration(P,SSGNMNT_RDR,_,_,_,_,PH4).
%position_in(D,S,P,SSGNMNT_RDR,T..T+PH4) :- patient(P,_), assignment(P,SSGNMNT_RDR,D,T), registration(P,SSGNMNT_RDR,_,_,_,_,PH4), x_e5ad5465_7192_45a1_9799_2256b9e658ec(D,S,P,SSGNMNT_RDR,T).
:- #count{D1: position_in(D,S,D1,_,TS), seat(S,_), day(D,_), timeslot(TS,_)} >= 2, day(D,_), timeslot(TS,_), seat(S,_).
:- assignment_to(_,_,_,TMSLT_SSGNMNT), TMSLT_SSGNMNT <= 23, DRTN_F_TH_FRTH_PHS > 50, registration(RGSTRTN_D,RGSTRTN_RDR,_,_,_,_,DRTN_F_TH_FRTH_PHS), assignment_to(RGSTRTN_D,RGSTRTN_RDR,_,TMSLT_SSGNMNT).
:~ patient(P,T), position_in(_,S,P,_,_), seat(S,T). [1@3,T,T]
