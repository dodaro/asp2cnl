:- (360 - granularity)/360 != (AI)/360, rotation(_,_,A,AI,_), (A)/360 = (0)/360.

% It is prohibited that the difference between 360, and granularity is different from AI, whenever there is a rotation with desired_angle A equal to 0, with current_angle AI.
% --> Non funziona

% It is required that the difference between 360, and granularity is equal to the current angle AI of the rotation R, whenever there is a rotation R with desired angle A equal to 0, and with current angle AI.
% --> Funziona
% Valutare se mettere "the current angle AI of the rotation R"