%vGUESS(0..999).
%vC_P(D, I, C_IP) :- vGUESS(X).

%{vC_P(D, I, C_IP): vGUESS(C_IP), vQ(D, I, Q_I), C_IP <= Q_I, vCREG_MINUS(D, I, CREG_IM), CREG_IM <= C_IP} = 1 :- time(I), date(D).
%{vC_M(D, I, C_IM): vGUESS(C_IM), vP(D, I, P_I), C_IM <= P_I} = 1 :- time(I), date(D).
%{vE_P1(D, I, E_IP1): vGUESS(E_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= E_IP1} = 1 :- time(I), date(D).
%{vE_M1(D, I, E_IM1): vGUESS(E_IM1)} = 1 :- time(I), date(D).
%{vS_P1(D, I, S_IP1): vGUESS(S_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= S_IP1} = 1 :- time(I), date(D).
%{vS_M1(D, I, S_IM1): vGUESS(S_IM1)} = 1 :- time(I), date(D).

%:~ A = PUN_I * C_IP,  vPUN(D, I, PUN_I), vC_P(D, I, C_IP). [A@1, I]
:~ A = (PZ_I * C_IM) / 1000,  vC_M(D, I, C_IM), vPZ(D, I, PZ_I). [-A@1, I]