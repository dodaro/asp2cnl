% topmovie(K) :- 1 <= #sum{VL: scoreassignment(X,VL)} <= 2, topmovie(K).
:~ #sum{VL: scoreassignment(_, VL)} = X , topmovie(Y). [Y@2]