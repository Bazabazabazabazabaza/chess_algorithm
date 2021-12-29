import chess
import random
import numpy as np
import timer_setup as ts
import chess_bot as BOT

board=chess.Board()

board2=board.copy()

chosen_move=board.parse_uci("g1f3")
board.push(chosen_move)
chosen_move=board2.parse_uci("g2g4")
board2.push(chosen_move)

board3=board.copy()
chosen_move=board.parse_uci("g7g5")
board.push(chosen_move)
chosen_move=board3.parse_uci("h7h5")
board3.push(chosen_move)


print(board)
print(board2)
print(board3)

print (board3.legal_moves)
print(list(board3.legal_moves)[2])
board_fen=str(board.fen).replace("<bound method Board.fen of Board('","").split()[0]
board_str=str(board).replace("\n","").replace(" ","") 
print(board_fen)
print(board_str)
print(board_str[2:4])
print (board.is_attacked_by(0,1),board.is_attacked_by(1,1))