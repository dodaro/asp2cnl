{match(X,Y)} :- set("set1",X), set("set2",Y).
positive_match(X,Y) :- Y < X, match(X,Y).
negative_match(X,Y) :- Y > X, match(X,Y).
:- #count{E,MTCH_SCND: match(E,MTCH_SCND)} != 1, set("set1",E).
:- #count{MTCH_FRST,E: match(MTCH_FRST,E)} != 1, set("set2",E).
%:- #count{PSTVMTCH_FRST,PSTVMTCH_SCND: positive_match(PSTVMTCH_FRST,PSTVMTCH_SCND)} = X_211196D9_B206_49E4_84C6_A21E423B3815, #count{NGTVMTCH_FRST,NGTVMTCH_SCND: negative_match(NGTVMTCH_FRST,NGTVMTCH_SCND)} = X_27DC87E1_53CE_4E7A_908E_052B2C091D92, X_211196D9_B206_49E4_84C6_A21E423B3815 != X_27DC87E1_53CE_4E7A_908E_052B2C091D92.
:- #count{X,Y: positive_match(X,Y), negative_match(T,Y)} = Z, #count{T,V: negative_match(T,V)} = K.