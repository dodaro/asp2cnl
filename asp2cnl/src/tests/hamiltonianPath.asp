node(1).
node(2).
node(3).
color("red").
color("green").
color("blue").
connectedto(1,2).
connectedto(1,3).
connectedto(2,1).
connectedto(2,3).
connectedto(3,1).
connectedto(3,2).
1 <= {assignedto(ND_D,CLR_D): color(CLR_D)} <= 1 :- node(ND_D).
:- connectedto(X,Y), assignedto(X,C), assignedto(Y,C).
