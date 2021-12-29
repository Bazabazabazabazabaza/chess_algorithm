import chess
import random
from chess_bot import *
import sys
import numpy

#multi moves algo with
#	-positional evaluation
# 	-cut off at game_over dead ends
#	-alpha-beta pruning	
#	-prioritize captures in search tree for faster a/b pruning

# to do:
#	-Monte carlo search tree?
#	-iterative search? (1, then 2 then 3 etc remembering the best move from previous seraches and testing them first.)
#	-serching until no captures instead of until certain depth
#	-Improve location values


price_dict={"P":1,"p":-1,"N":3,"n":-3,"B":3.1,"b":-3.1,"R":5,"r":-5,"Q":9,"q":-9,"K":0,"k":0}
square_adress_fen={	"a8":0,"b8":1,"c8":2,"d8":3,"e8":4,"f8":5,"g8":6,"h8":7,
				"a7":8,"b7":9,"c7":10,"d7":11,"e7":12,"f7":13,"g7":14,"h7":15,
				"a6":16,"b6":17,"c6":18,"d6":19,"e6":20,"f6":21,"g6":22,"h6":23,
				"a5":24,"b5":25,"c5":26,"d5":27,"e5":28,"f5":29,"g5":30,"h5":31,
				"a4":32,"b4":33,"c4":34,"d4":35,"e4":36,"f4":37,"g4":38,"h4":39,
				"a3":40,"b3":41,"c3":42,"d3":43,"e3":44,"f3":45,"g3":46,"h3":47,
				"a2":48,"b2":49,"c2":50,"d2":51,"e2":52,"f2":53,"g2":54,"h2":55,
				"a1":56,"b1":57,"c1":58,"d1":59,"e1":60,"f1":61,"g1":62,"h1":63}
square_adress_pychess={	"a1":0,"b1":1,"c1":2,"d1":3,"e1":4,"f1":5,"g1":6,"h1":7,
				"a2":8,"b2":9,"c2":10,"d2":11,"e2":12,"f2":13,"g2":14,"h2":15,
				"a3":16,"b3":17,"c3":18,"d3":19,"e3":20,"f3":21,"g3":22,"h3":23,
				"a4":24,"b4":25,"c4":26,"d4":27,"e4":28,"f4":29,"g4":30,"h4":31,
				"a5":32,"b5":33,"c5":34,"d5":35,"e5":36,"f5":37,"g5":38,"h5":39,
				"a6":40,"b6":41,"c6":42,"d6":43,"e6":44,"f6":45,"g6":46,"h6":47,
				"a7":48,"b7":49,"c7":50,"d7":51,"e7":52,"f7":53,"g7":54,"h7":55,
				"a8":56,"b8":57,"c8":58,"d8":59,"e8":60,"f8":61,"g8":62,"h8":63}

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
	#board_fen=str(board.fen).replace("<bound method Board.fen of Board('","").split()[0]
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
	
	
	def __init__(self,board,parent_move,ID,parent_ID,player_color,move,shalowness):
		self.board			=board				
		self.parent_move	=parent_move				
		self.ID				=ID				
		self.parent_ID		=parent_ID				
		self.player_color	=player_color	
		self.children = []
		self.children_str = []
		self.current_color=self.board.turn 
		ev=eval_static_board(self.board,self.player_color)
		self.eval=ev[0]
		self.game_over=ev[1]
		self.global_eval=self.eval
		self.turn=self.board.fullmove_number
		self.shalowness=shalowness
		self.move_str=move
		self.best_move=None


	def generate_children(self):
		for move_count,move in enumerate(self.board.legal_moves,0):
			
			self.board.push(move)
			child_board=self.board.copy()
			self.board.pop()

			move_str=move.uci()
			if move_str in self.children_str:
				pass
			else:
				self.children +=[move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,self.shalowness)]
				self.children_str +=[move_str]
		self.shalowness+=1
		#if self.parent_move!=None:
		#	self.parent_move.shalowness+=1

		glo_eval=0
		#for child in self.children:

		return

	def generate_child(self,move):
			
		self.board.push(move)
		child_board=self.board.copy()
		self.board.pop()
		move_str=move.uci()
		if move_str in self.children_str:
			pass
		else:
			self.children +=[move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,self.shalowness)]
			self.children_str +=[move_str]

		#self.shalowness+=1
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
		return

	def eval_global_white(self,alpha,beta): 
		factor =1# (-1+2*self.player_color)
		#print("eval_global_white "+str(self.move_str)+" "+str(self.shalowness)+" "+str(self.board.move_stack))
		offturn=0
		if (-1+2*self.player_color)*(-1+2*self.current_color)==-1:
			offturn=1

		


		legal_move_list=[]
		move_list_benef=[]
		board_str=str(self.board).replace("\n","").replace(" ","")
		color_to_move_factor=-1+2*self.board.turn
		for move_count,move in enumerate(self.board.legal_moves,0):
			move_str=move.uci()
			benef=0

			if self.board.is_capture(move)==True:
				if self.board.is_en_passant(move)==True:
					benef=10.
				else:
					benef=10.-color_to_move_factor*(price_dict[board_str[square_adress_fen[move_str[2:4]]]]+price_dict[board_str[square_adress_fen[move_str[0:2]]]])
					#print(self.board)
					#print(move_str,square_adress_fen[move_str[2:4]],square_adress_fen[move_str[0:2]],benef)
					#print(board_str[square_adress_fen[move_str[2:4]]],board_str[square_adress_fen[move_str[0:2]]])
			if self.board.is_attacked_by(1-self.board.turn,square_adress_pychess[move_str[2:4]]):
				benef-=color_to_move_factor*price_dict[board_str[square_adress_fen[move_str[0:2]]]]

			if self.board.is_attacked_by(self.board.turn,square_adress_pychess[move_str[2:4]]):
				benef+=0.5

			if len(legal_move_list)!=0:
				if benef<=move_list_benef[-1]:
					move_list_benef.append(benef)
					legal_move_list.append(move)
				else:		
					for ind,ben in enumerate(move_list_benef,0):
						if benef>ben:
							move_list_benef.insert(ind,benef)
							legal_move_list.insert(ind,move)
							break
			else:
				legal_move_list=[move]
				move_list_benef=[benef]

		if offturn==0:
			self.global_eval=-1000

			for move_count,move in enumerate(legal_move_list,0):
				move_str=move.uci()
				child=None
				if move_str in self.children_str:
					child=self.children[self.children_str.index(move_str)]
					
				else:
					self.board.push(move)
					child_board=self.board.copy()
					self.board.pop()

					shalow=max(0,self.shalowness-1)

					child=move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,shalow)
					self.children +=[child]
					self.children_str +=[move_str]

				if self.shalowness!=0:
					child.eval_global_white(alpha,beta)
				self.global_eval=factor*max(self.global_eval,child.global_eval)
				alpha=max(alpha,child.global_eval)
				if beta<=alpha:
					#print("pruning on move")
					break				


		else:
			self.global_eval=1000

			for move_count,move in enumerate(legal_move_list,0):
				move_str=move.uci()
				child=None
				if move_str in self.children_str:
					child=self.children[self.children_str.index(move_str)]
					
				else:
					self.board.push(move)
					child_board=self.board.copy()
					self.board.pop()

					shalow=max(0,self.shalowness-1)

					child=move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,shalow)					
					self.children +=[child]
					self.children_str +=[move_str]

			
				if self.shalowness!=0:
					child.eval_global_white(alpha,beta)
				self.global_eval=factor*min(self.global_eval,child.global_eval)
				beta=min(beta,child.global_eval)
				if beta<=alpha:
					#print("pruning off move")
					break

		self.shalowness+=1
		#if self.parent_move!=None:
		#	self.parent_move.shalowness+=1
		return

	def eval_global_black(self,alpha,beta):
		factor =1# (-1+2*self.player_color)

		offturn=0
		if (-1+2*self.player_color)*(-1+2*self.current_color)==-1:
			offturn=1
		
		legal_move_list=[]
		move_list_benef=[]
		board_str=str(self.board).replace("\n","").replace(" ","")
		color_to_move_factor=-1+2*self.board.turn
		for move_count,move in enumerate(self.board.legal_moves,0):
			move_str=move.uci()
			benef=0

			if self.board.is_capture(move)==True:
				if self.board.is_en_passant(move)==True:
					benef=10.
				else:
					benef=10.-color_to_move_factor*(price_dict[board_str[square_adress_fen[move_str[2:4]]]]+price_dict[board_str[square_adress_fen[move_str[0:2]]]])
					#print(self.board)
					#print(move_str,square_adress_fen[move_str[2:4]],square_adress_fen[move_str[0:2]],benef)
					#print(board_str[square_adress_fen[move_str[2:4]]],board_str[square_adress_fen[move_str[0:2]]])
			#if self.board.is_attacked_by(1-self.player_color,square_adress_pychess[move_str[2:4]]):
			if self.board.is_attacked_by(1-self.board.turn,square_adress_pychess[move_str[2:4]]):
				benef-=color_to_move_factor*price_dict[board_str[square_adress_fen[move_str[0:2]]]]

			#if self.board.is_attacked_by(self.player_color,square_adress_pychess[move_str[2:4]]):
			if self.board.is_attacked_by(self.board.turn,square_adress_pychess[move_str[2:4]]):
				benef=0.5

			if len(legal_move_list)!=0:
				if benef<=move_list_benef[-1]:
					move_list_benef.append(benef)
					legal_move_list.append(move)
				else:		
					for ind,ben in enumerate(move_list_benef,0):
						if benef>ben:
							move_list_benef.insert(ind,benef)
							legal_move_list.insert(ind,move)
							break
			else:
				legal_move_list=[move]
				move_list_benef=[benef]
		#print(str(self.board))
		#print(move_list_benef)
		#list_print=[]
		#for stuff in legal_move_list:
		#	list_print+=[stuff.uci()]
		#print(list_print)
		#print(len(list(self.board.legal_moves))-len(list_print))

		if offturn==0:
			self.global_eval=1000
			for move_count,move in enumerate(legal_move_list,0):
				move_str=move.uci()
				child=None
				if move_str in self.children_str:
					child=self.children[self.children_str.index(move_str)]
					
				else:
					self.board.push(move)
					child_board=self.board.copy()
					self.board.pop()

					shalow=max(0,self.shalowness-1)

					child=move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,shalow)
					self.children +=[child]
					self.children_str +=[move_str]

				if self.shalowness!=0:
					child.eval_global_black(alpha,beta)
				self.global_eval=factor*min(self.global_eval,child.global_eval)
				alpha=min(alpha,child.global_eval)
				if beta>=alpha:
					break

		else:
			self.global_eval=-1000
			for move_count,move in enumerate(legal_move_list,0):
				move_str=move.uci()
				child=None
				if move_str in self.children_str:
					child=self.children[self.children_str.index(move_str)]
					
				else:
					self.board.push(move)
					child_board=self.board.copy()
					self.board.pop()

					shalow=max(0,self.shalowness-1)

					child=move_unit(child_board,self,move_count,self.ID,self.player_color,move_str,shalow)					
					self.children +=[child]
					self.children_str +=[move_str]

				if self.shalowness!=0:
					child.eval_global_black(alpha,beta)

				self.global_eval=factor*max(self.global_eval,child.global_eval)
				beta=max(beta,child.global_eval)
				if beta>=alpha:
					break

		self.shalowness+=1

		return


	def delete_children(self):
		if self.shalowness>0:
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
				del(child)
			else:
				new_children=[child]
		self.children=new_children
		return

class uni_move_eval_bot: 
	init=0

	def build_architecture(self):
		print("Building globeval 5 architecture")
		
		if self.player_color==0:
			max_stuff=self.deapth
		else:
			max_stuff=self.deapth-1

		for i in range(0,max_stuff):
			if self.player_color==1:
				alpha=-1000
				beta=1000
				self.root_move.eval_global_white(alpha,beta)
			if self.player_color==0:
				alpha=1000
				beta=-1000
				self.root_move.eval_global_black(alpha,beta)
		
		global_eval=-1000
		if self.player_color==0:
			global_eval=1000
		move=self.root_move

		#offturn=0
		#if (-1+2*self.player_color)*(-1+2*self.current_color)==-1:
		#	offturn=1
		#if off_move==1:
		for child in self.root_move.children:
			if self.player_color==0:
				if child.global_eval<global_eval:
					global_eval=child.global_eval
					move=child
			elif self.player_color==1:
				if child.global_eval>global_eval:
					global_eval=child.global_eval
					move=child
		self.root_move.global_eval=global_eval
		self.root_move.best_move=move

		#self.root_move.generate_children()
		#for i in range(0,self.deapth):
		#	self.root_move.deepen_1lvl()

		print("Done building globeval 5 architecture")
		return move

	def __init__(self,color,board,deapth):
		self.player_color=color
		self.board=board.copy()
		self.root_move=move_unit(self.board,None,0,0,self.player_color,"origin",0)
		self.deapth=deapth
		self.alpha=0
		self.beta=0
		self.build_architecture()

	def update_architecture(self,move,catch_up):
		move_str=move.uci()
		self.root_move.chose_and_trim(move_str)
		if move_str in self.root_move.children_str:
			self.root_move=self.root_move.children[0]
		else:
			self.root_move.generate_child(move)
			self.root_move=self.root_move.children[0]

		#self.root_move.build_architecture()
		#self.root_move.deepen_1lvl()
		if catch_up==0:
			
			if self.player_color==1:
				alpha=-1000
				beta=1000
				self.root_move.eval_global_white(alpha,beta)
			if self.player_color==0:
				alpha=1000
				beta=-1000
				self.root_move.eval_global_black(alpha,beta)
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
			print("Catching globeval 5 up")
			catch_up=1
			for ind in range(0,move_diff):
				#print(move_stack[-move_diff+ind])
				self.update_architecture(move_stack[-move_diff+ind],catch_up)
			print("Done catching globeval 5 up")

			if board!=self.board:
				print("ERROR:updated board is not up to date: \n"+str(board)+"\n"+str(self.board)) 
				sys.exit()

		print("searching globeval 5 move")
		
		if self.player_color==1:
			alpha=-1000
			beta=1000
			self.root_move.eval_global_white(alpha,beta)
		if self.player_color==0:
			alpha=1000
			beta=-1000
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
			#print(child.move_str,child.eval,child.global_eval,global_eval) # Randomize the choice of moves with same eval
			#elif child.global_eval==global_eval:
			#	if random.choice([0,1])==1:
			#		move=child
		print("from eval_bot color and globeval 5: ",self.player_color, global_eval,move.move_str, self.root_move.shalowness) 

		######## USEFUL DEBUG PRINTS ############
		#print(self.board.legal_moves)
		#glo_list=[]
		#glo_list2=[]
		#for chil in self.root_move.children:
		#	glo_list+=[(chil.move_str,chil.global_eval,chil.shalowness)]
		#print(glo_list,glo_list2)
		######## USEFUL DEBUG PRINTS ############
		
		catch_up=0
		if list(board.legal_moves)[0].from_uci(move.move_str) not in board.legal_moves: 
			print("chosen move "+move.move_str+" is not legal. Picking first legal move insetad.")
			self.update_architecture(list(board.legal_moves)[0],catch_up)
			return list(board.legal_moves)[0]
		else:
			self.update_architecture(list(board.legal_moves)[0].from_uci(move.move_str),catch_up)
			return list(board.legal_moves)[0].from_uci(move.move_str)
		print("after update color and globeval: ",self.player_color, global_eval,move.move_str, self.root_move.shalowness)

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
