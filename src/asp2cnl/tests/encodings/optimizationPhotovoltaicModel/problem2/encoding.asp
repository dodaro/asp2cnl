vGUESS(0..999).

%%%%  GUESS VARIABILI DI DECISIONE
{vP_L(D, I, P_L): vGUESS(P_L)} = 1 :- time(I), date(D).
{vP_PV(D, I, P_PV): vGUESS(P_PV)} = 1 :- time(I), date(D).
{vP_S(D, I, P_S): vGUESS(P_S)} = 1 :- time(I), date(D).

%%%% FUNZIONE OBIETTIVO
%:~ F = P_L - P_PV - P_S, vP_L(D, I, P_L), vP_PV(D, I, P_PV), vP_S(D, I, P_S).  [F@1, I]
:~ vP_L(D, I, P_L).  [P_L@1, I]
:~ vP_PV(D, I, P_PV).  [-P_PV@1, I]
:~ vP_S(D, I, P_S).  [-P_S@1, I]

%%%% VINCOLI
%% E_Smin <= E_S_t_d + P_S_t_d * deltaT <= E_Smax
%:- E_SMIN - E_SINIT  > #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I} > E_SMAX - E_SINIT, date(D), vE_Sinit(E_SINIT), vE_Smin(E_SMIN), vE_Smax(E_SMAX).
% WORKS WITH CNL
auxvP_S(D, I,  I * P_S) :- vP_S(D, I, P_S).
:- DIFF_MIN = E_SMIN - E_SINIT - 1, DIFF_MAX = E_SMAX - E_SINIT + 1, DIFF_MAX  <= #sum{P_S: auxvP_S(D, I, P_S)} <= DIFF_MIN, date(D), vE_Sinit(E_SINIT), vE_Smin(E_SMIN), vE_Smax(E_SMAX).

%% P_Smin <= PS_t_d <= P_Smax
:- P_SMIN > P_S, P_S > P_SMAX, vP_S(D, I, P_S), vP_Smin(P_SMIN), vP_Smax(P_SMAX).

