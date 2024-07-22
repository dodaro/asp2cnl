:- topMovie(SCORE), SCORE - 5 >= 0.
:- topMovie(SCORE), topMovie(SCORE2), SCORE - SCORE2 >= 0.
:- topMovie(SCORE), topMovie(SCORE2), SCORE - SCORE2 >= 0, movie(SCORE3), movie(SCORE4), bestMovie(SCORE5), SCORE3 - SCORE4 = SCORE5.
:- movie(SCORE), bestmovie(SCORE2), SCORE >= 0, SCORE2 >= 0, SCORE < SCORE2.


:- movie(SCORE), movie(SCORE2), 0 <= SCORE, SCORE2 >= SCORE.
:- movie(SCORE), bestMovie(SCORE2), SCORE + SCORE2 + 1 > 0.
:- movie(SCORE), bestMovie(SCORE2), SCORE + 2 + 1 > 0.
:- movie(SCORE), bestMovie(SCORE2), 0 < SCORE + 2 + 1.
:- movie(SCORE), movie(SCORE2), 0 + 1 + SCORE <= SCORE2, 1 > SCORE, SCORE >= SCORE2.

:- C1 = C2, assignment(X,C1), assignment(Y,C2), edge(X,Y).

:~ assignment(VALUE, TARGET). [VALUE-TARGET@5]
:~ assignment(VALUE, 1), assignment(TARGET, 2). [VALUE-TARGET@5]
:~ movie(D), topMovie(D1). [-D@3]
:~ #count{D: movie(D)} = X. [-X@3]
:~ #count{D: movie(D)} = X, topMovie(K). [-X@3]

