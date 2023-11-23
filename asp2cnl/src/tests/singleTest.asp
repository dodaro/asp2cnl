%:- topmovie(1), #sum{VLL,X: scoreassignment(X,VLL)} <= 2.

:- topmovie(1), #sum{VLL: scoreassignment(X,VLL), topmovie(X)} <= 2.

