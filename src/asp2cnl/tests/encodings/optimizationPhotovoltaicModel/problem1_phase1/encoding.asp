vGUESS(0..999).

%%%%  GUESS VARIABILI DI DECISIONE
{vC_P(D, I, C_IP): vGUESS(C_IP), vQ(D, I, Q_I), C_IP <= Q_I, vCREG_MINUS(D, I, CREG_IM), CREG_IM <= C_IP} = 1 :- time(I), date(D).
{vC_M(D, I, C_IM): vGUESS(C_IM), vP(D, I, P_I), C_IM <= P_I} = 1 :- time(I), date(D).
{vE_P1(D, I, E_IP1): vGUESS(E_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= E_IP1} = 1 :- time(I), date(D).
{vE_M1(D, I, E_IM1): vGUESS(E_IM1)} = 1 :- time(I), date(D).
{vS_P1(D, I, S_IP1): vGUESS(S_IP1), vCREG_MINUS(D, I, CREG_IM), CREG_IM <= S_IP1} = 1 :- time(I), date(D).
{vS_M1(D, I, S_IM1): vGUESS(S_IM1)} = 1 :- time(I), date(D).


%%%% FUNZIONE OBIETTIVO
:~ A = PUN_I * C_IP,  vPUN(D, I, PUN_I), vC_P(D, I, C_IP). [A@1, I]
:~ A = (PZ_I * C_IM) / 1000,  vC_M(D, I, C_IM), vPZ(D, I, PZ_I). [-A@1, I]
:~ B = COSTCHARGE1 * S_IP1, vCostCharge1(COSTCHARGE1), vS_P1(D, I, S_IP1). [B@1, I]
:~ B = COSTDISCHARGE1 * S_IM1, vCostDischarge1(COSTDISCHARGE1), vS_M1(D, I, S_IM1). [B@1, I]
:~ C = PAP + E_IP1, vPAP(PAP), vE_P1(D, I, E_IP1). [-C@1, I]
:~ D = PVP + E_IM1, vPVP(PVP), vE_M1(D, I, E_IM1), E = POFF_IP * CREG_IP, vPOFF_PLUS(D, I, POFF_IP), vCREG_PLUS(D, I, CREG_IP), F = POFF_IM * CREG_IM, vPOFF_MINUS(D, I, POFF_IM), vCREG_MINUS(D, I, CREG_IM). [D-E-F@1, I]


%%%% VINCOLI

%% C_IP - C_IM = (Q_I - P_I) + S_I1 + E_I1 - CREG_IM + CREG_IP
% :- #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2: vS_M1(D, I, S_IM1); E_IP1,3: vE_P1(D, I, E_IP1); -E_IM1,4: vE_M1(D, I, E_IM1); -C_IP,5: vC_P(D, I, C_IP); C_IM,6: vC_M(D, I, C_IM)} != P_I - Q_I + CREG_IM - CREG_IP, vCREG_MINUS(D, I, CREG_IM), vCREG_PLUS(D, I, CREG_IP), vQ(D, I, Q_I), vP(D, I, P_I).
% WORKS IN CNL
:- SUM_S_IP1 = #sum{S_IP1: vS_P1(D, I, S_IP1)},
  SUM_S_IM1 = #sum{S_IM1: vS_M1(D, I, S_IM1)},
  SUM_E_IP1 = #sum{E_IP1: vE_P1(D, I, E_IP1)},
  SUM_E_IM1 = #sum{E_IM1: vE_M1(D, I, E_IM1)},
  SUM_C_IP = #sum{C_IP: vC_P(D, I, C_IP)},
  SUM_C_IM = #sum{C_IM: vC_M(D, I, C_IM)},
  SUM_ALL = SUM_S_IP1 - SUM_S_IM1 + SUM_E_IP1 - SUM_E_IM1 - SUM_C_IP + SUM_C_IM,
  SUM_ALL != P_I - Q_I + CREG_IM - CREG_IP,
 vCREG_MINUS(D, I, CREG_IM), vCREG_PLUS(D, I, CREG_IP), vQ(D, I, Q_I), vP(D, I, P_I).

%% CREG_IM <= S_IP1 + E_IP1 + C_IP
% :-vCREG_MINUS(D, I, CREG_IM),  CREG_IM != 0, CREG_IM > #sum{S_IP1, 1: vS_P1(D, I, S_IP1); E_IP1,2: vE_P1(D, I, E_IP1); C_IP,3: vC_P(D, I, C_IP)}.
% WORKS IN CNL
:- CREG_IM != 0,  SUM_S_IP1 = #sum{S_IP1: vS_P1(D, I, S_IP1)}, SUM_E_IP1 = #sum{E_IP1: vE_P1(D, I, E_IP1)}, SUM_C_IP = #sum{C_IP,3 : vC_P(D, I, C_IP)},
                            CREG_IM > SUM_S_IP1 + SUM_E_IP1 + SUM_C_IP,  vCREG_MINUS(D, I, CREG_IM).

%% E_IP1 <= OVER_I * Percentage_Ps1
:- E_IP1 * 10 > (OVER_I * PERCENTAGE_PS1) , vE_P1(D, I, E_IP1), vOVER_I(D, I, OVER_I), vPercentage_Ps1(PERCENTAGE_PS1).


%% E_IM1 <= UNDER_I * Percentage_Ms1
:- E_IM1 * 10 > (UNDER_I * PERCENTAGE_MS1), vE_M1(D, I, E_IM1), vUNDER_I(D, I, UNDER_I), vPercentage_Ms1(PERCENTAGE_MS1).


%% EMin1 <= S_IP1 - S_IM1 <= EMax1
% :- EMIN1 > #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2:vS_M1(D, I, S_IM1)} > EMAX1, vEMin1(EMIN1), vEMax1(EMAX1).
% WORKS IN CNL
:-  SUM_S_IP1 = #sum{S_IP1,1: vS_P1(D, I, S_IP1)}, SUM_S_IM1 =  #sum{S_IM1,2:vS_M1(D, I, S_IM1)}, SUM_ALL = SUM_S_IP1 - SUM_S_IM1, EMIN1 > SUM_ALL, SUM_ALL > EMAX1, vEMin1(EMIN1), vEMax1(EMAX1).

%% CAP_TOT_MIN_1 <= SSOC_I + S_IP1 - S_IM1 <= CAP_TOT_MAX_1
% :- vSOC(D, 0, SOC_I), #sum{S_IP1,1: vS_P1(D, I, S_IP1); -S_IM1,2: vS_M1(D, I, S_IM1)} > CAP_TOT_MAX_1 - SOC_I,  vCapTotMax_1(CAP_TOT_MAX_1).
% WORKS IN CNL
:- vSOC(D, 0, SOC_I), SUM_S_IP1 = #sum{S_IP1,1: vS_P1(D, I, S_IP1)}, SUM_S_IM1 =  #sum{S_IM1,2: vS_M1(D, I, S_IM1)}, SUM_ALL = SUM_S_IP1 - SUM_S_IM1, SUM_ALL > CAP_TOT_MAX_1 - SOC_I,  vCapTotMax_1(CAP_TOT_MAX_1).

%% EMinS1 <= E_IP1 - E_IM1 <= EMaxS1
% :- vEMinS1(EMINS1), EMINS1 > #sum{E_IP1,1: vE_P1(D, I, E_IP1); -E_IM1,2: vE_M1(D, I, E_IM1)} > EMAXS1, vEMaxS1(EMAXS1).
% WORKS IN CNL
:- vEMinS1(EMINS1), SUM_E_IP1 = #sum{E_IP1: vE_P1(D, I, E_IP1)}, SUM_E_IM1 = #sum{E_IM1: vE_M1(D, I, E_IM1)}, SUM_ALL = SUM_E_IP1 - SUM_E_IM1, EMINS1 > SUM_ALL, SUM_ALL > EMAXS1, vEMaxS1(EMAXS1).


%% CAP_TOT_MIN_S1 <= SOC_SI + E_IP1 - E_IM1 <= CAP_TOT_MAX_S1
% :- #sum{E_IP1,1 : vE_P1(D, I, E_IP1); -E_IM1,2: vE_M1(D, I, E_IM1)} > CAP_TOT_MAX_S1 - SOC_SI, vSOC_S(D, 0, SOC_SI), vCapTotMax_S1(CAP_TOT_MAX_S1).
% WORKS IN CNL
:- SUM_E_IP1 = #sum{E_IP1: vE_P1(D, I, E_IP1)}, SUM_E_IM1 = #sum{E_IM1: vE_M1(D, I, E_IM1)}, SUM_ALL = SUM_E_IP1 - SUM_E_IM1, SUM_ALL > CAP_TOT_MAX_S1 - SOC_SI, vSOC_S(D, 0, SOC_SI), vCapTotMax_S1(CAP_TOT_MAX_S1).

%% 0 <= Percentage_Ps1 <= 1
:- vPercentage_Ps1(PERCENTAGE_PS1), PERCENTAGE_PS1 > 10.

%% 0 <= Percentage_Ms1 <= 1
:- vPercentage_Ms1(PERCENTAGE_MS1), PERCENTAGE_MS1 > 10.

vOVER_I(D, I, OVER_I) :- P_I >= Q_I, OVER_I = P_I - Q_I, vP(D, I, P_I), vQ(D, I, Q_I).
vOVER_I(D, I, 0) :- P_I < Q_I, vP(D, I, P_I), vQ(D, I, Q_I).
vUNDER_I(D, I, UNDER_I) :- P_I <= Q_I, UNDER_I = Q_I - P_I, vP(D, I, P_I), vQ(D, I, Q_I).
vUNDER_I(D, I, 0) :- P_I > Q_I, vP(D, I, P_I), vQ(D, I, Q_I).

