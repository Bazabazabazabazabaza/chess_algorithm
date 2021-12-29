import chess
import chess.svg
import random
import datetime
import numpy as np
import timer_setup as ts
import time
import chess_bot as M1_BOT
import chess_eval_bot as BOT1
import chess_eval_bot_v2 as BOT2
import chess_eval_bot_v3 as BOT3
import chess_eval_bot_v4 as BOT4
import chess_eval_bot_v5 as BOT5

timer=ts.Timer()
timer.start()

board=chess.Board()

#print("Test prints:")
#print(board.legal_moves)
#print(list(board.legal_moves)[0])
#print()
#print()
print()


def interpret_result(result1,board):
	if result1=="1/2-1/2":
		if (board.is_seventyfive_moves()==1): 
			return 2
		else:
			if board.is_insufficient_material()==1:
				return 3
			elif board.is_stalemate()==1:
				return 4
			else:
				return 0
	elif result1=="0-1":
		return -1
	elif result1=="1-0":
		return 1

def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


nb_games=1
max_moves=1000
Rgames_outcomes=np.zeros((nb_games))



print_outcome=0

for game in range(0,nb_games):
	print("--- Starting game "+str(game)+" ---")
	board.reset()

	#black_BOT=BOT.random_bot()
	#black_BOT=BOT.uni_move_lvl5_bot()
	#black_BOT=BOT.human_move()
	#black_BOT=BOT.uni_move_lvl4_bot()
	white_BOT=BOT5.uni_move_eval_bot(1,board,3)
	#white_BOT=BOT.uni_move_lvl4_bot()
	black_BOT=BOT5.uni_move_eval_bot(0,board,3)

	move_count=0

	game_timer_start = time.perf_counter()
	white_time=0
	black_time=0

	while board.is_game_over()==0:
	#	print(move_count,board.move_stack)
		print(move_count,move_count%2)
		print(board)
		chess.svg.board(board, size=350)
		board
		if move_count%2==0:
			white_timer_start = time.perf_counter()
			chosen_move=white_BOT.chose_move(board)
			white_timer_stop = time.perf_counter()
			ti=white_timer_stop - white_timer_start
			print("turn took "+str(ti)+"s")
			white_time += ti
		elif move_count%2==1:
			black_timer_start = time.perf_counter()
			chosen_move=black_BOT.chose_move(board)
			black_timer_stop = time.perf_counter()
			ti=black_timer_stop - black_timer_start
			print("turn took "+str(ti)+"s")
			black_time += ti
		move_count+=1

		#possible_moves=list(board.legal_moves)
		#chosen_move=random.choice(possible_moves)
		if board.has_insufficient_material(board.turn)==1:
			Rgames_outcomes[game]=-100+200*(1-board.turn)
			break


		board.push(chosen_move)

		#if board.fullmove_number>75:
		#	print("main ", board.fullmove_number,board.outcome(),board.is_seventyfive_moves())


		if (board.outcome()!=None or board.fullmove_number>max_moves):
			#print(board.outcome(winner))
			if print_outcome==1:
				print(interpret_result(board.result()))
				print(board)
				

			if board.fullmove_number>max_moves:
				Rgames_outcomes[game]=2
				break
			else:
				Rgames_outcomes[game]=interpret_result(board.result(),board)
	
	game_timer_end = time.perf_counter()
	print(board)
	print(board.outcome(),board.result(),"game time:",game_timer_end- game_timer_start,"white time",white_time,"black time",black_time)
	
	output_file="save_stacks.txt"
	now = datetime.datetime.now()
	with open(output_file,"a+") as file:
		file.write("\n\n"+str(now)+"\n"+(str(board.move_stack).replace("Move.from_uci(","").replace(")","")+"\n"+"game time:"+str(game_timer_end- game_timer_start)+" white time "+str(white_time)+" black time "+str(black_time)+"\n\n"))

print(Rgames_outcomes)
nb_Black_wins=countX(Rgames_outcomes,-1)
nb_White_wins=countX(Rgames_outcomes,1)
nb_Black_wins+=countX(Rgames_outcomes,-100)
nb_White_wins+=countX(Rgames_outcomes,100)
nb_black_checkmates=countX(Rgames_outcomes,-1)
nb_white_checkmates=countX(Rgames_outcomes,1)
nb_Draws=countX(Rgames_outcomes,0)
nb_Draws+=countX(Rgames_outcomes,2)
nb_Draws+=countX(Rgames_outcomes,3)
nb_Draws+=countX(Rgames_outcomes,4)
nb_75moves=countX(Rgames_outcomes,2)
nb_insuficient_mat=countX(Rgames_outcomes,3)
nb_stalemates=countX(Rgames_outcomes,4)


print("white wins,  Draw,  Black wins")
print(nb_White_wins,nb_Draws,nb_Black_wins)
print(float(nb_White_wins)/float(nb_games),float(nb_Draws)/float(nb_games),float(nb_Black_wins)/float(nb_games))
print()
print("white CM,  Black CM")
print(nb_white_checkmates,nb_black_checkmates)
print()
print("75 moves, insuf. mat., stalemates")
print(nb_75moves, nb_insuficient_mat, nb_stalemates)

timer.stop()
