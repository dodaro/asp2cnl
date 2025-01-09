vGUESS(0..999).
%%%%  GUESS VARIABILI DI DECISIONE
{vS_P_i_j(D, I, J, S_P_I_J): vGUESS(S_P_I_J)} = 1 :- time(I), date(D), user(J).
{vS_M_i_j(D, I, J, S_M_I_J): vGUESS(S_M_I_J)} = 1 :- time(I), date(D), user(J).
{vC_P_i_j(D, I, J, C_P_I_J): vGUESS(C_P_I_J)} = 1 :- time(I), date(D), user(J).
{vC_M_i_j(D, I, J, C_M_I_J): vGUESS(C_M_I_J)} = 1 :- time(I), date(D), user(J).


%%%% FUNZIONE OBIETTIVO
:~ vS_P_i_j(D, I, J, S_P_I_J). [S_P_I_J@1, I, J]
:~ vS_M_i_j(D, I, J, S_M_I_J). [S_M_I_J@1, I, J]
:~ vC_P_i_j(D, I, J, C_P_I_J). [C_P_I_J@1, I, J]
:~ vC_M_i_j(D, I, J, C_M_I_J). [C_M_I_J@1, I, J]


%%%% VINCOLI
%:- #sum{S_P_I_J, J, 1: vS_P_i_j(D, I, J, S_P_I_J); -S_M_I_J, J, 2: vS_M_i_j(D, I, J, S_M_I_J)} != CHARGING_I, vCHARGING_i(D, I, CHARGING_I).
% WORKS IN CNL
:- SUM_S_P_I_J = #sum{S_P_I_J, J: vS_P_i_j(D, I, J, S_P_I_J)}, SUM_S_M_I_J = #sum{S_M_I_J, J: vS_M_i_j(D, I, J, S_M_I_J)}, SUM_ALL = SUM_S_P_I_J - SUM_S_M_I_J, SUM_ALL != CHARGING_I, vCHARGING_i(D, I, CHARGING_I).

%:- #sum{C_M_I_J, 1: vC_M_i_j(D, I, J, C_M_I_J); Q_I_J, 2: vQ_i_j(D, I, J, Q_I_J); -P_I_J, 3: vP_i_j(D, I, J, P_I_J); S_P_I_J, 4: vS_P_i_j(D, I, J, S_P_I_J); -S_M_I_J, 5: vS_M_i_j(D, I, J, S_M_I_J)} != C_P_I_J, vC_P_i_j(D, I, J, C_P_I_J).
% WORKS IN CNL
:- SUM_C_M_I_J = #sum{C_M_I_J: vC_M_i_j(D, I, J, C_M_I_J)}, SUM_Q_I_J = #sum{Q_I_J: vQ_i_j(D, I, J, Q_I_J)}, SUM_P_I_J = #sum{P_I_J: vP_i_j(D, I, J, P_I_J)}, SUM_S_P_I_J = #sum{S_P_I_J: vS_P_i_j(D, I, J, S_P_I_J)}, SUM_S_M_I_J = #sum{S_M_I_J: vS_M_i_j(D, I, J, S_M_I_J)}, SUM_ALL = SUM_C_M_I_J + SUM_Q_I_J - SUM_P_I_J + SUM_S_P_I_J - SUM_S_M_I_J, SUM_ALL != C_P_I_J, vC_P_i_j(D, I, J, C_P_I_J).

:- C_P_I_J > Q_I_J + S_P_I_J, vC_P_i_j(D, I, J, C_P_I_J), vS_P_i_j(D, I, J, S_P_I_J), vQ_i_j(D, I, J, Q_I_J).

:- C_M_I_J > P_I_J + S_M_I_J, vC_M_I_J(D, I, J, C_M_I_J), vS_M_i_j(D, I, J, S_M_I_J), vP_i_j(D, I, J, P_I_J).

%:- #sum{S_P_I_J, I, 1: vS_P_i_j(D, I, J, S_P_I_J); -S_M_I_J, I, 2: vS_M_i_j(D, I, J, S_M_I_J)} > EMAX_J, vEMax_j(D, J, EMAX_J).
% WORKS IN CNL
:- SUM_S_P_I_J = #sum{S_P_I_J, I: vS_P_i_j(D, I, J, S_P_I_J)}, SUM_S_M_I_J = #sum{S_M_I_J, I: vS_M_i_j(D, I, J, S_M_I_J)}, SUM_ALL = SUM_S_P_I_J - SUM_S_M_I_J, SUM_ALL > EMAX_J, vEMax_j(D, J, EMAX_J).

%:- #sum{S_P_I_J, I, 1: vS_P_i_j(D, I, J, S_P_I_J); -S_M_I_J, I, 2: vS_M_i_j(D, I, J, S_M_I_J)} > CAPTOP_J - RE_J, user(J), vCapTot_j(D, J, CAPTOP_J), vRE_j(D, 0, J, RE_J).
% WORKS IN CNL
:- SUM_S_P_I_J = #sum{S_P_I_J, I: vS_P_i_j(D, I, J, S_P_I_J)}, SUM_S_M_I_J = #sum{S_M_I_J, I: vS_M_i_j(D, I, J, S_M_I_J)}, SUM_ALL = SUM_S_P_I_J - SUM_S_M_I_J, SUM_ALL > CAPTOP_J - RE_J, user(J), vCapTot_j(D, J, CAPTOP_J), vRE_j(D, 0, J, RE_J).
