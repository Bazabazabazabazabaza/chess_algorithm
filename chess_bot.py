import chess
import random

def piece_price(piece):
	price=0
	if str(piece)=="p" or str(piece)=="P":
		price=1
	elif str(piece)=="n" or str(piece)=="N":
		price=3
	elif str(piece)=="b" or str(piece)=="B":
		price=4
	elif str(piece)=="r" or str(piece)=="R":
		price=5
	elif str(piece)=="q" or str(piece)=="Q":
		price=9
	elif str(piece)=="k" or str(piece)=="K":
		price=10
	return price

def move_is_stalemate(board,move):
	board.push(move)
	if board.is_stalemate()==1:
		board.pop()
		return 1
	else:
		board.pop()
		return 0

class uni_move_lvl1_bot(): 
	#This bot checks all curent legal moves and choses moves in this order of priority:
	#-capture (most expensive piece) (will take if able)
	#-random if no capture available.

	def chose_move(self,board):
		possible_moves=list(board.legal_moves)

		chosen_square_price=0
		move_chosen=0
		chosen_move=possible_moves[0]

		for move_count,moves in enumerate(board.legal_moves,0):
			
			if(board.is_capture(moves)):
				price=piece_price(board.piece_at(moves.to_square))
				if chosen_square_price<price:
					chosen_square_price=price
					chosen_move=moves

				move_chosen=1
				
		if move_chosen==0:
			chosen_move=random.choice(possible_moves)
		return chosen_move


class uni_move_lvl2_bot(): 
	#This bot checks all curent legal moves and choses moves in this order of priority:
	#-checkmate move
	#-capture (will take if the targetted piece is of higher cost than the taking piece)
	#-random if no checkmate or capture available.

	def chose_move(self,board):
		possible_moves=list(board.legal_moves)

		chosen_square_price=0
		move_chosen=0
		chosen_move=possible_moves[0]

		for move_count,moves in enumerate(board.legal_moves,0):
			
			if (board.gives_check(moves)):
				board.push(moves)
				if board.is_checkmate()==1:
					board.pop()
					return moves
				else:
					board.pop()
					pass

			if(board.is_capture(moves)):
				price=piece_price(board.piece_at(moves.to_square))
				if chosen_square_price<price:
					chosen_square_price=price
					chosen_move=moves

				move_chosen=1
				
		if move_chosen==0:
			chosen_move=random.choice(possible_moves)
		return chosen_move

class uni_move_lvl3_bot(): 
	#This bot checks all curent legal moves and choses moves in this order of priority:
	#-checkmate move
	#-capture (will take if the targetted piece is of higher 
	#	cost than the taking piece or if the attacked piece is undefended)
	#-random if no checkmate or capture available but doe not move to attacked squares if able.

	def chose_move(self,board):
		color=board.turn
		oponent_color=1-color
		possible_moves=list(board.legal_moves)

		chosen_square_price=0
		move_chosen=0
		chosen_move=possible_moves[0]

		if (board.fullmove_number==1 and color==1):
			chosen_move=random.choice(["Nf3", "Nc3", "e3", "d3"])

		for move_count,moves in enumerate(board.legal_moves,0):
			
			if (board.gives_check(moves)):
				board.push(moves)
				if board.is_checkmate()==1:
					board.pop()
					return moves
				else:
					board.pop()
					pass
			
			#should be: if piece not defended price = price
			#           if piece defended:
			if(board.is_capture(moves)):
				price=piece_price(board.piece_at(moves.to_square))
				if chosen_square_price<price or board.is_attacked_by(oponent_color,moves.to_square)==0:
					chosen_square_price=price
					chosen_move=moves
					move_chosen=1

		if move_chosen==0:
			# Defend, find pins, sqewers, forks and attacks, avoid terrible moves

			moves_selection=[]
			for move_count,moves in enumerate(board.legal_moves,0):
				if board.is_attacked_by(oponent_color,moves.to_square)==1:
					pass
				else:
					moves_selection+=[moves.uci()]

			if len(moves_selection)==0:
				chosen_move=random.choice(possible_moves)
			else:
				chosen_move=moves.from_uci(random.choice(moves_selection))

		return chosen_move


class uni_move_lvl4_bot(): 
	#This bot checks all curent legal moves and choses moves in this order of priority:
	#-checkmate move
	#-capture (will take if the targetted piece is of higher 
	#			cost than the taking piece or if the attacked piece is undefended)
	#-random if no checkmate or capture available but doe not move to attacked squares if able.
	#			Priorities moving pieces under attack to safety (highest cost first)


	def chose_move(self,board):
		color=board.turn
		oponent_color=1-color
		possible_moves=list(board.legal_moves)

		chosen_square_price=0
		move_chosen=0
		chosen_move=possible_moves[0]

		
		for move_count,moves in enumerate(board.legal_moves,0):
			
			if (board.gives_check(moves)):
				board.push(moves)
				if board.is_checkmate()==1:
					board.pop()
					return moves
				else:
					board.pop()
					pass
			
			#should be: if piece not defended price = price
			#           if piece defended:
			if(board.is_capture(moves)):
				price=piece_price(board.piece_at(moves.to_square))
				if chosen_square_price<price or board.is_attacked_by(oponent_color,moves.to_square)==0:
					chosen_square_price=price
					chosen_move=moves
					move_chosen=1

		if move_chosen==0:
			# Defend, find pins, sqewers, forks and attacks, avoid terrible moves

			moves_selection=[]
			nb_moves_in_selection=0
			values=[]
			valued=0
			for move_count,moves in enumerate(board.legal_moves,0):
				if board.is_attacked_by(oponent_color,moves.to_square)==1:
					pass
				else:
					if board.is_attacked_by(oponent_color,moves.from_square)==1:
						values+=[ piece_price(board.piece_at(moves.from_square)) ]
						moves_selection+=[move_count]
						nb_moves_in_selection+=1
						valued=1
					else:
						values+=[0]
						moves_selection+=[move_count]
						nb_moves_in_selection+=1


			


			if nb_moves_in_selection==0:
				chosen_move=random.choice(possible_moves)
			else:
				choice=0
				if valued==1:
					maxval=0
					for count,prices in enumerate(values,0):
						if prices>maxval:
							maxval=prices
							choice=count
				else:
					choice=random.randint(1,nb_moves_in_selection)-1
				
				for move_count,moves in enumerate(board.legal_moves,0):
					if move_count==moves_selection[choice]:
						chosen_move=moves
						break

		return chosen_move


def checkmate_in_N(board_input,N):
	board=board_input.copy()
	stock_move=chess.Move(chess.A1,chess.B1)

	for move_count,moves in enumerate(board.legal_moves,0):
		board.push(moves)
		if board.is_checkmate()==1:
			board.pop()
			#print("CM in N head",N,moves)
			return (1,moves)
		else:
			board.pop()
			pass

	if N-1<=0:
		return (1000,stock_move.from_uci("0000"))
	
	best_mate=(1000,stock_move)
	for move_count,moves in enumerate(board.legal_moves,0):
		mate=1

		board.push(moves)
		mate_speed=0
		for move_count2,moves2 in enumerate(board.legal_moves,0):
			
			board.push(moves2)
			outcome =checkmate_in_N(board,N-1)
			if outcome==(1000,stock_move.from_uci("0000")):
				mate=0
				board.pop()
				break
			else:
				if outcome[0]>mate_speed and outcome[0]!=1000:
					mate_speed=outcome[0]
				pass
			board.pop()

		if mate==1:
			if mate_speed+1<best_mate[0] and mate_speed!=0:
				best_mate=(mate_speed+1,moves)
		board.pop()


	if (best_mate!=(1000,stock_move)):
		return best_mate
	else:
		return (1000,stock_move.from_uci("0000"))





class uni_move_lvl5_bot(): 
	#This bot checks all curent legal moves and choses moves in this order of priority:
	#-If first move, play e4, d4, Nf3 or Nc3
	#-detects fastest checkmate several moves ahead(2 or 3 (higher is very expensive))
	#-detects and avoids fastest enemy checkmate several moves ahead(2 or 3 (higher is very expensive))
	#-capture (will take if the targetted piece is of higher 
	#			cost than the taking piece or if the attacked piece is undefended)
	#-random if no checkmate or capture available 
	#			but does not move to attacked squares if able.
	#			Priorities moving pieces under attack to safety (highest cost first)
	#			avoid stalemates	


	# To do: 	
	#			-detect potential forks
	#			-detect pins and skewers
	#			-avoid running into mate in ones
	#			-



	def chose_move(self,board):
		color=board.turn
		oponent_color=1-color
		possible_moves=list(board.legal_moves)

		chosen_square_price=0
		move_chosen=0
		chosen_move=possible_moves[0]

		if (board.fullmove_number==1 and color==1):
			chosen_move_str=random.choice(["g1f3", "b1c3", "e2e4", "d2d4"])
			chosen_move=board.parse_uci(chosen_move_str)
			#print(chosen_move)
			return chosen_move

		#Check checkmates


		
		mate_check=1
		if board.fullmove_number>50:
			mate_check=2
		stock_move=chess.Move(chess.A1,chess.B1)

		if board.fullmove_number>4:
			result=checkmate_in_N(board,mate_check)
			move=result[1]  
			#print(board.fullmove_number,move)

			if move!=stock_move.from_uci("0000"):
				print("FOUND IT!",result)
				print(board)

				return move

		black_listed_moves=[]
		mate_check=1
		for move_count,moves in enumerate(board.legal_moves,0):
			board.push(moves)
			move1=checkmate_in_N(board,mate_check)[1]
			if move1!=stock_move.from_uci("0000"):
				print("prevent_mate!",moves)
				black_listed_moves+=[1]
			else:
				black_listed_moves+=[0]

			board.pop()



		
		for move_count,moves in enumerate(board.legal_moves,0):
			if black_listed_moves[move_count]==1:
				continue
			#if (board.gives_check(moves)):
			#	board.push(moves)
			#	if board.is_checkmate()==1:
			#		board.pop()
			#		return moves
			#	else:
			#		board.pop()
			#		pass
			
			#should be: if piece not defended price = price
			#           if piece defended:
			if(board.is_capture(moves)):
				price=piece_price(board.piece_at(moves.to_square))
				if chosen_square_price<price or board.is_attacked_by(oponent_color,moves.to_square)==0:
					chosen_square_price=price
					chosen_move=moves
					move_chosen=1

		if move_chosen==0:
			# Defend, find pins, sqewers, forks and attacks, avoid terrible moves

			moves_selection=[]
			nb_moves_in_selection=0
			values=[]
			valued=0
			for move_count,moves in enumerate(board.legal_moves,0):
				if black_listed_moves[move_count]==1:
					continue

				if move_is_stalemate(board,moves)==1:
					pass
				elif board.is_attacked_by(oponent_color,moves.to_square)==1: # if target square is attacked, don't go
					pass
				else:
					if board.is_attacked_by(oponent_color,moves.from_square)==1: #if the starting square is attacked, leave
						values+=[ piece_price(board.piece_at(moves.from_square)) ]
						moves_selection+=[move_count]
						nb_moves_in_selection+=1
						valued=1
					else:
						values+=[0]
						moves_selection+=[move_count]
						nb_moves_in_selection+=1

					if len(board.attackers(color,moves.to_square))>=2: #if the target square is protected, it's better 
						values[-1]+=1			
			


			if nb_moves_in_selection==0:
				chosen_move=random.choice(possible_moves)
			else:
				choice=0
				if valued==1:
					maxval=0
					for count,prices in enumerate(values,0):
						if prices>maxval:
							maxval=prices
							choice=count
				else:
					choice=random.randint(1,nb_moves_in_selection)-1
				
				for move_count,moves in enumerate(board.legal_moves,0):
					if black_listed_moves[move_count]==1:
						continue
					if move_count==moves_selection[choice]:
						chosen_move=moves
						break

		return chosen_move

class human_move(): 
	def chose_move(self,board):
		print("Play your move!")
		print("Are allowed:",board.legal_moves)
		val = input("Enter your value: ")
		while list(board.legal_moves)[0].from_uci(val) not in board.legal_moves:
			print("not a legal move!")
			val = input("Enter your value: ")

		return list(board.legal_moves)[0].from_uci(val)

#test section
#board=chess.Board()
#bot=1_move_BOT()

