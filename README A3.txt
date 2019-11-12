Introducing Alpha-Beta pruning reduced the amount of time it took to generate a move
in the minimax player in every trial I ran. I noticed the first move always took the longest
because there were so many trees to explore, and AB Pruning reduced the time it took to
generate the first move from 16.89 seconds to 5.63 seconds. The full list of move times
for multiple trials are listed below.

Time Trials:

Attempt 1
Minimax moves - 16.89, 2.93, 0.15
AlphaBetaMinimax moves - 5.63, 0.58, 0.04

Attempt 2
Minimax first move - 12.63, 0.82, 0.02
AlphaBetaMinimax - 3.19, 0.19, 0.02

Attempt 3
Minimax first move - 12.59, 0.73, 0.05
AlphaBetaMinimax - 2.85, 0.20, 0.01