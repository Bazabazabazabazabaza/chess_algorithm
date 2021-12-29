import chess
import random
from chess_bot import *
import sys
import numpy

#multi moves algo with positional evaluation and cut off at game_over dead ends.

price_dict={"P":1,"p":-1,"N":3,"n":-3,"B":3.1,"b":-3.1,"R":5,"r":-5,"Q":9,"q":-9,"K":0,"k":0}

def piece_location(piece,square):
	color_factor = 1-(1-piece.isupper())*2
	location_value=0
	if piece=="n" or piece=="N":
		if square in [28,29,36,37]:
			location_value=0.012
		elif square in [19,20,21,22,27,30,35,38,43,44,45,46]:
			location_value=0.01
		elif square%8==1 or square%8==0:
			location_value=-0.05
	elif piece=="k" or piece=="K":
		if square in [1,2,3,7,8,63,64,57,58,59]:
			location_value=0.2
		if square in [9,10,11,12,13,14,15,16,49,50,51,52,53,54,55,56]:
			location_value=-0.1

	elif piece=="p" or piece=="P":

		if square in [28,29,36,37]:
			location_value=0.01

		
	elif piece=="b" or piece=="B":
		if (square-1)/8==0:
			location_value+=-0.01
		elif (square-1)/8==7:
			location_value+=-0.01

	return location_value*color_factor

def piece_price(piece,square):

	price=0.0
	if str(piece)==".":
		pass
	else:
		price=price_dict[str(piece)]
	price+=piece_location(piece,square)    

	return price

def eval_static_board(board,board_color):
	board_fen=str(board.fen).replace("<bound method Board.fen of Board('","").split()[0]
	board_str=str(board).replace("\n","").replace(" ","") 
	evalu=0

	#print(board_str)

	game_over=0
	if board.result()=="0-1":
		evalu= -100
		game_over=1
	elif board.result()=="1-0":
		evalu= 100
		game_over=1
	elif board.result()==" 1/2-1/2":
		evalu= 0
		game_over=1
	else:
		for sq_nb,squares in enumerate(board_str,1):
			evalu+=piece_price(squares,sq_nb)

	#eval=(-1+2*board_color)*eval
	#print(eval)
	return [evalu,game_over]

class move_unit():
	
	def __init__(self,board,parent_move,ID,parent_ID,player_color,move):
		self.board			=board				
		self.parent_move	=parent_move				
		self.ID				=ID				
		self.parent_ID		=parent_ID				
		self.player_color	=player_color	
		self.children = []
		self.current_color=self.board.turn 
		ev=eval_static_board(self.board,self.player_color)
		self.eval=ev[0]
		self.game_over=ev[1]
		self.global_eval=self.eval
		self.turn=self.board.fullmove_number
		self.shalowness=0
		self.move_str=move


	def generate_children(self):
		for move_count,move in enumerate(self.board.legal_moves,0):
			
			self.board.push(move)
			child_board=self.board.copy()
			self.board.pop()

			child_move_denomination=str(self.current_color)+"_"+str(self.turn)+"_parent"+str(self.parent_ID)+"_"+str(self.ID)
			#exec(child_move_denomination+"=move_unit(child_board,self,move_count,self.ID,self.player_color,move.uci())")
			#vars()[child_move_denomination]=move_unit(child_board,self,move_count,self.ID,self.player_color)

			#self.children += [child_move_denomination]
			self.children +=[move_unit(child_board,self,move_count,self.ID,self.player_color,move.uci())]
		self.shalowness+=1
		#if self.parent_move!=None:
		#	self.parent_move.shalowness+=1

		glo_eval=0
		#for child in self.children:


		return

	def deepen_1lvl(self):
		if self.game_over!=1:
			for child in self.children:
				if child.shalowness==0:
					child.generate_children()
				else:
					child.deepen_1lvl()
		self.shalowness+=1

		return

	def eval_global_white(self,alpha,beta):
		factor =1# (-1+2*self.player_color)

		offturn=0
		if (-1+2*self.player_color)*(-1+2*self.current_color)==-1:
			offturn=1

		
		if offturn==0:
			self.global_eval=-1000
			for child in self.children:
				if child.shalowness!=0:
					child.eval_global_white(alpha,beta)
				self.global_eval=factor*max(self.global_eval,child.global_eval)
				#alpha=max(alpha,child.global_eval)
				#if beta<=alpha:
				#	break

		else:
			self.global_eval=1000
			for child in self.children:
				if child.shalowness!=0:
					child.eval_global_white(alpha,beta)
				self.global_eval=factor*min(self.global_eval,child.global_eval)
				#beta=min(beta,child.global_eval)
				#if beta<=alpha:
				#	break
		return

	def eval_global_black(self,alpha,beta):
		factor =1# (-1+2*self.player_color)

		offturn=0
		if (-1+2*self.player_color)*(-1+2*self.current_color)==-1:
			offturn=1

		
		if offturn==0:
			self.global_eval=1000
			for child in self.children:
				if child.shalowness!=0:
					child.eval_global_black(alpha,beta)
				self.global_eval=factor*min(self.global_eval,child.global_eval)
				#alpha=max(alpha,child.global_eval)
				#if beta<=alpha:
				#	break

		else:
			self.global_eval=-1000
			for child in self.children:
				if child.shalowness!=0:
					child.eval_global_black(alpha,beta)
				self.global_eval=factor*max(self.global_eval,child.global_eval)
				#beta=min(beta,child.global_eval)
				#if beta<=alpha:
				#	break
		return


	def delete_children(self):
		if self.shalowness>1:
			for child in self.children:
				child.delete_children()
				del(child)
		else:
			for child in self.children:
				del(child)
		return

	def chose_and_trim(self,move_str):
		new_children=[]
		for child in self.children:
			if child.move_str!=move_str:
				child.delete_children()
				if len(self.children)!=1:
					del(child)
				else:
					new_children=[child]
			else:
				new_children=[child]
		self.children=new_children
		return

class uni_move_eval_bot: 
	init=0

	def build_architecture(self):
		self.root_move.generate_children()
		for i in range(0,self.deapth-1):
			self.root_move.deepen_1lvl()
		return

	def __init__(self,color,board,deapth):
		self.player_color=color
		self.board=board.copy()
		self.root_move=move_unit(self.board,None,0,0,self.player_color,"origin")
		self.deapth=deapth
		self.alpha=0
		self.beta=0
		self.build_architecture()

	def update_architecture(self,move):
		
		self.root_move.chose_and_trim(move.uci())
		self.root_move=self.root_move.children[0]
		self.root_move.deepen_1lvl()
		self.board.push(move)




		return 

	def chose_move(self,board):
		move_stack=board.move_stack
		if board.turn!=self.player_color:
			print("ERROR: player color and turn do not match:"+str(self.player_color)+"!="+str(board.turn))
			print(board,board.move_stack)
			sys.exit()

		if board!=self.board:
			move_stack=board.move_stack
			move_diff=len(move_stack)-len(self.board.move_stack)

			#print(move_stack, self.board.move_stack, move_diff)

			for ind in range(0,move_diff):
				#print(move_stack[-move_diff+ind])
				self.update_architecture(move_stack[-move_diff+ind])

			if board!=self.board:
				print("ERROR:updated board is not up to date: \n"+str(board)+"\n"+str(self.board)) 
				sys.exit()

		alpha=-1000
		beta=1000
		if self.player_color==1:
			self.root_move.eval_global_white(alpha,beta)
		if self.player_color==0:
			self.root_move.eval_global_black(alpha,beta)
		
		global_eval=-1000
		if self.player_color==0:
			global_eval=1000
		move=self.root_move
		
		for child in self.root_move.children:
			if self.player_color==0:
				if child.global_eval<global_eval:
					global_eval=child.global_eval
					move=child
			elif self.player_color==1:
				if child.global_eval>global_eval:
					global_eval=child.global_eval
					move=child
			#print(child.move_str,child.eval,child.global_eval,global_eval)
			#elif child.global_eval==global_eval:
			#	if random.choice([0,1])==1:
			#		move=child
		print("from eval_bot color and globeval 3: ",self.player_color, global_eval,move.move_str, self.root_move.shalowness) 
		print(self.board.legal_moves)
		glo_list=[]
		glo_list2=[]
		for chil in self.root_move.children:
			glo_list+=[(chil.move_str,chil.global_eval,chil.shalowness)]
		print(glo_list,glo_list2)
		
		if list(board.legal_moves)[0].from_uci(move.move_str) not in board.legal_moves: 
			print("chosen move "+move.move_str+" is not legal. Picking first legal move insetad.")
			self.update_architecture(list(board.legal_moves)[0])
			return list(board.legal_moves)[0]
		else:
			self.update_architecture(list(board.legal_moves)[0].from_uci(move.move_str))
			return list(board.legal_moves)[0].from_uci(move.move_str)

"""
board=chess.Board()
eval_static_board(board,0)
board.remove_piece_at(chess.A1)
board.remove_piece_at(chess.C8)
board.remove_piece_at(chess.C2)
board.remove_piece_at(chess.D1)
eval_static_board(board,0)
eval_static_board(board,1)
print(board.turn)
original=move_unit(board,None,0,0,board.turn,"")"""
