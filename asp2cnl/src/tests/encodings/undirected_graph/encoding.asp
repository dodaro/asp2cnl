1 <= {assigned_to(ND_D,ST_D,ND_WGHT): set(ST_D)} <= 1 :- node(ND_D,ND_WGHT).
:- node(N1,SSGND_T_WGHT), assigned_to(N1,S1,SSGND_T_WGHT), node(N2,SSGND_T_WGHT1), assigned_to(N2,S1,SSGND_T_WGHT1), set(S1), edge(N1,N2).

%:- #count{D: assigned_to(D,S1,_), set(S1)} = X_31009C1A_DF1A_4E68_A1C6_96241F53184B, #count{D1: assigned_to(D1,S2,_), set(S2)} = X_6F271D73_3794_44CE_8740_27B0A0035347, X_31009C1A_DF1A_4E68_A1C6_96241F53184B <= X_6F271D73_3794_44CE_8740_27B0A0035347, S1 = 1, S2 = 2.
:- #count{D: assigned_to(D,S1,_), set(S1)} = Y, #count{D1: assigned_to(D1,S2,_), set(S2)} = X, Y <= X, S1 = 1, S2 = 2.

:- #sum{WGHT: assigned_to(_,S2,WGHT), set(S2)} = X_87CC864C_071D_42D7_97CB_18E25E4CB03B, #sum{WGHT1: assigned_to(_,S1,WGHT1), set(S1)} = X_BDC2C474_8F05_44F8_8C14_9262BDFDF973, X_87CC864C_071D_42D7_97CB_18E25E4CB03B < X_BDC2C474_8F05_44F8_8C14_9262BDFDF973, S1 = 1, S2 = 2.
