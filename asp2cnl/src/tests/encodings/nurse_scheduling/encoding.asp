%%%%% input %%%%%

total_days(365).
% day(1..365).

% workshift(id, name, hours).
workshift(1,"1_morning",7).
workshift(2,"2_afternoon",7).
workshift(3,"3_night",10).
workshift(4,"4_restafternights",0).
workshift(5,"5_rest",0). %called weekend in the document.
workshift(6,"6_holiday",0).

%%%%% encoding %%%%%

% Choose an assignment for each day and for each nurse.
1 <= {assign(N, T, D) : workshift(T,_,_)} <= 1 :- day(D), nurse(N).

% Each nurse works from 1687 to 1692 hours per year.
:- nurse(N), maxHoursPerYear(MAX), #sum{H,D : assign(N,T,D), workshift(T,_,H)} > MAX.
:- nurse(N), minHoursPerYear(MIN), #sum{H,D : assign(N,T,D), workshift(T,_,H)} < MIN.

% Each nurse cannot work twice in 24 hours.
:- nurse(N), assign(N, T1, D), assign(N, T2, D+1), T2 < T1, T2 <= 3, T1 <= 3.

% Exactly (or at least, to check) 30 days of holidays.
%:- nurse(N), #count{D:assign(N,6,D)} < 30.
:- nurse(N), #count{D:assign(N,6,D)} != 30.

% After two consecutive nights there is one rest day.
:- not assign(N,4,D), assign(N,3,D-2), assign(N,3,D-1).
:- assign(N,4,D), not assign(N,3,D-2).
:- assign(N,4,D), not assign(N,3,D-1).

% At least 2 rest days each 14 days.
:- nurse(N), day(D), total_days(DAYS), D <= DAYS-13, #count{D1:assign(N,5,D1), D1>=D, D1 < D+14} < 2.

% Each morning the number of nurses can range from 6 to 9.
:- day(D), #count{N:assign(N,1,D)} > K, maxNurseMorning(K).
:- day(D), #count{N:assign(N,1,D)} < K, minNurseMorning(K).

% Each afternoon the number of nurses can range from 6 to 9.
:- day(D), #count{N:assign(N,2,D)} > K, maxNurseAfternoon(K).
:- day(D), #count{N:assign(N,2,D)} < K, minNurseAfternoon(K).

% Each night the number of nurses can range from 4 to 7.
:- day(D), #count{N:assign(N,3,D)} > K, maxNurseNight(K).
:- day(D), #count{N:assign(N,3,D)} < K, minNurseNight(K).

% Fair distribution (morning, afternoon, night)
% ---> morning
:- nurse(N), #count{D : assign(N,1,D)} > MAXDAYS, maxDays(MAXDAYS).
:- nurse(N), #count{D : assign(N,1,D)} < MINDAYS, minDays(MINDAYS).
% ---> afternoon
:- nurse(N), #count{D : assign(N,2,D)} > MAXDAYS, maxDays(MAXDAYS).
:- nurse(N), #count{D : assign(N,2,D)} < MINDAYS, minDays(MINDAYS).
% ---> night
:- nurse(N), #count{D : assign(N,3,D)} > MAXNIGHTS, maxNights(MAXNIGHTS).
:- nurse(N), #count{D : assign(N,3,D)} < MINNIGHTS, minNights(MINNIGHTS).

% #show assign/3.
