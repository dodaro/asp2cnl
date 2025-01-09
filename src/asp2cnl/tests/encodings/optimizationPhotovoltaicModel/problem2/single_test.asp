% :- E_SMIN - E_SINIT  > #sum{P_SP: vP_S(D, I, P_S), P_SP = P_S * I} > E_SMAX - E_SINIT, date(D), vE_Sinit(E_SINIT), vE_Smin(E_SMIN), vE_Smax(E_SMAX).

 auxvP_S(D, I,  I * P_S) :- vP_S(D, I, P_S).
 :- DIFF_MIN = E_SMIN - E_SINIT - 1, DIFF_MAX = E_SMAX - E_SINIT + 1, DIFF_MAX  <= #sum{P_S: auxvP_S(D, I, P_S)} <= DIFF_MIN, date(D), vE_Sinit(E_SINIT), vE_Smin(E_SMIN), vE_Smax(E_SMAX).
