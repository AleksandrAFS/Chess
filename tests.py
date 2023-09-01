from board import Board
#Test 1
b = Board()
b[1][0].move(3, 0)
b[6][7].move(4, 7)
b[3][0].move(4, 0)
b[4][7].move(3, 7)
b[4][0].move(5, 0)
b[3][7].move(2, 7)
b[5][0].move(6, 1)
b[2][7].move(1, 6)
b[6][1].move(7, 2)
b[1][6].move(0, 5)
b[7][2].move(7, 3)
b[0][4].move(0, 5)
b[6][0].move(4, 0)
b[7][2].move(7, 3)
print(b)
b.surrender()
#output:

#♜ ♞ . ♕ ♚ ♝ ♞ ♜
#. . ♟ ♟ ♟ ♟ ♟ .
#. . . . . . . .
#♟ . . . . . . .
#. . . . . . . .
#. . . . . . . .
#. ♙ ♙ ♙ ♙ ♙ . ♙
#♖ ♘ ♗ ♕ . ♔ ♘ ♖
