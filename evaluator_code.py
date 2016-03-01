''' 

This is the engine for the Ultimate TicTacToe Tournament. The code in this file is not for reproduction.
@author: Devansh Shah

The structure of the code is as below:
1. Header Files
2. Sample implementations of your class (Player and ManualPlayer)
3. Game Logic
4. Game simulator

In case of any queries, please post on moodle.iiit.ac.in

'''

import sys
import random
import signal

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class ManualPlayer:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		


class Player1:
	
	def __init__(self):
		self.max_depth = 4
		pass

	def move(self, board, block, old_move, flag):
		valid_blocks = self.blocks_allowed(old_move, block)
		if len(valid_blocks) != 0:
			bl = valid_blocks[random.randrange(len(valid_blocks))]
		else:
			print "here"
			bl = block.index('-')
		tboard = []
		for i in range(9):
			new = []
			for j in range(9):
				new.append(board[i][j])
			tboard.append(new)
		cell = self.alphabeta(tboard, bl, flag, flag, 0, -1000, 1000)
		return cell

	def heuristic(self, board,block_number,player):
		x_start = (block_number/3)*3
		y_start = (block_number%3)*3
		heuristic_value = 0
		# for i in range(3):
		# 	for j in range(3):
		# 		board[x_start+i][y_start+j]=raw_input()
		
		# for i in range(3):
		# 	for j in range(3):
		# 		print board[x_start+i][y_start+j],
		# 	print "\n"

		#horizontal check
		for i in range(3):
			x = x_start + i
			y = y_start
			count_of_empty_cells = 0
			for j in range(3):
				y = y_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start + i
			y = y_start 
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1]):
					heuristic_value+=100
				elif board[x][y]!=player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1]):
					heuristic_value-=100
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x][y+1] and board[x][y]==player) or (board[x][y+1]==board[x][y+2] and board[x][y+1]==player) or (board[x][y]==board[x][y+2] and board[x][y]==player) :
					heuristic_value+=10
				elif (board[x][y]==board[x][y+1] and board[x][y]!=player) or (board[x][y+1]==board[x][y+2] and board[x][y+1]!=player) or (board[x][y]==board[x][y+2] and board[x][y]!=player): 
					heuristic_value-=10
			elif count_of_empty_cells==2:
				if board[x][y]==player or board[x][y+1]==player or board[x][y+2]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1	
		#print heuristic_value,"horizontal"
		#vertical check						
		for i in range(3):
			x = x_start
			y = y_start + i
			count_of_empty_cells = 0
			for j in range(3):
				x = x_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start
			y = y_start + i
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y]):
					heuristic_value+=100
				elif board[x][y]!=player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y]):
					heuristic_value-=100
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x+1][y] and board[x][y]==player) or (board[x+1][y]==board[x+2][y] and board[x+1][y]==player) or (board[x][y]==board[x+2][y] and board[x][y]==player) :
					heuristic_value+=10
				elif (board[x][y]==board[x+1][y] and board[x][y]!=player) or (board[x+1][y]==board[x+2][y] and board[x+1][y]!=player) or (board[x][y]==board[x+2][y] and board[x][y]!=player): 
					heuristic_value-=10
			elif count_of_empty_cells==2:
				if board[x][y]==player or board[x+1][y]==player or board[x+2][y]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1
		#print heuristic_value,"vertical"
		#diagonal check 1
		count_of_empty_cells = 0
		x = x_start
		y = y_start
		if board[x_start][y_start]=='-':
			count_of_empty_cells+=1
		if board[x_start+1][y_start+1]=='-':
			count_of_empty_cells+=1
		if board[x_start+2][y_start+2]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x_start][y_start]==player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1]):
				heuristic_value+=100
			elif board[x_start][y_start]!=player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1]):
				heuristic_value-=100
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x+1][y+1] and board[x][y]==player) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y+1]==player) or (board[x][y]==board[x+2][y+2] and board[x][y]==player) :
				heuristic_value+=10
			elif (board[x][y]==board[x+1][y+1] and board[x][y]!=player) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y+1]!=player) or (board[x][y]==board[x+2][y+2] and board[x][y]!=player): 
				heuristic_value-=10
		elif count_of_empty_cells==2:
			if board[x_start][y_start]==player or board[x_start+1][y_start+1]==player or board[x_start+2][y_start+2]==player:
				heuristic_value+=1
			else:
				heuristic_value-=1

		#diagonal check 2
		count_of_empty_cells = 0
		x = x_start+2
		y = y_start
		if board[x][y]=='-':
			count_of_empty_cells+=1
		if board[x-1][y+1]=='-':
			count_of_empty_cells+=1
		if board[x-2][y+2]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x][y]==player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1]):
				heuristic_value+=100
			elif board[x][y]!=player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1]):
				heuristic_value-=100
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x-1][y+1] and board[x][y]==player) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y+1]==player) or (board[x][y]==board[x-2][y+2] and board[x][y]==player) :
				heuristic_value+=10
			elif (board[x][y]==board[x-1][y+1] and board[x][y]!=player) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y+1]!=player) or (board[x][y]==board[x-2][y+2] and board[x][y]!=player): 
				heuristic_value-=10
		elif count_of_empty_cells==2:
			if board[x][y]==player or board[x-1][y+1]==player or board[x-2][y+2]==player:
				heuristic_value+=1
			else:
				heuristic_value-=1

		#print "value", heuristic_value
		return heuristic_value

	def alphabeta(self, tboard, bl, flag, turn, depth, a, b):
		if depth == self.max_depth:
			return self.heuristic(tboard, bl, flag)
			#return random.randrange(200) - 100

		if turn == 'x':
			oturn = 'o'
		else:
			oturn = 'x'
		cells = []
		x = (bl/3)*3
		y = (bl%3)*3
		for i in range(3):
			p = x+i
			for j in range(3):
				q = y + j
				if tboard[p][q] == "-":
					cells.append((p,q)) 
				else:
					#print p, q, tboard[p][q]
					pass
		
		#print cells
		for i in range(len(cells)):
			if a > b:
				return util
			tboard[cells[i][0]][cells[i][1]] = turn
			h = self.heuristic(tboard, bl, flag)
			if h > 70:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay"
					good = 1
					return cells[i]
				return (self.max_depth - depth + 1)*100
			elif h < -70:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay1"
					pass
				else:
					return (self.max_depth - depth + 1)*-100
			v = self.alphabeta(tboard, bl, flag, oturn, depth+1, a, b)
			tboard[cells[i][0]][cells[i][1]] = "-"
			if i == 0:
				util = v
			if turn == flag:
				if v > a:
					a = v
					if depth == 0:
						move = cells[i]
				if v > util:
					util = v
			else:
				if v < b:
					b = v
				if v < util:
					util = v
		if cells == []:
			return self.heuristic(tboard, bl, flag)
		if depth == 0:
			return move
		return util


	def  blocks_allowed(self, old_move,block):
		if old_move[0]==-1 and old_move[1]==-1:
			return []
		if old_move[0]%3==0 and old_move[1]%3==0:
			block1 = 1
			block2 = 3
		elif old_move[0]%3==0 and old_move[1]%3==1:
			block1 = 0
			block2 = 2
		elif old_move[0]%3==0 and old_move[1]%3==2:
			block1 = 1
			block2 = 5
		elif old_move[0]%3==1 and old_move[1]%3==0:
			block1 = 0
			block2 = 6
		elif old_move[0]%3==1 and old_move[1]%3==1:
			block1 = 4
		elif old_move[0]%3==1 and old_move[1]%3==2:
			block1 = 2
			block2 = 8
		elif old_move[0]%3==2 and old_move[1]%3==0:
			block1 = 3
			block2 = 7
		elif old_move[0]%3==2 and old_move[1]%3==1:
			block1 = 6
			block2 = 8
		elif old_move[0]%3==2 and old_move[1]%3==2:
			block1 = 5
			block2 = 7

		if block1!=4:
			if block[block1]=='-' and block[block2]=='-':
				return [block1,block2]
			elif block[block1]=='-' and block[block2]!='-':
				return [block1]
			if block[block1]!='-' and block[block2]=='-':
				return [block2]
			if block[block1]!='-' and block[block2]!='-':
				return []
		else:
			if block[4]=='-':
				return [4]
			else:
				return []

	def cells_allowed(self, board, valid_blocks, block):
		cells = []
		for bl in valid_blocks:
			x = (bl/3)*3
			y = (bl%3)*3
			for i in range(3):
				a = x+i
				for j in range(3):
					b = y + j
					if board[a][b] == '-':
						cells.append((a,b))

		if cells == []:
			for bl in range(9):
				if block[bl] == '-':
					x = (bl/3)*3
					y = (bl%3)*3
					for i in range(3):
						a = x+i
						for j in range(3):
							b = y + j
							if board[a][b] == '-':
								cells.append((a,b))

		return cells

class Player12:
	
	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		#Choose a move based on some algorithm, here it is a random move.
		return cells[random.randrange(len(cells))]


class Player2(object):
	def __init__(self):
		self.max_depth = 4
		self.hv = []
		for i in range(3):
			new = []
			for j in range(3):
				new.append(0)
			self.hv.append(new)
		#print self.hv[2][2]
		#print type(self.hv[0])

	def move(self, board, block, old_move, flag):
		if old_move == (-1,-1):
			self.hv[1][1] = 0.04
			return (4,4)
			#print "first"
		x = old_move[0]/3
		y = old_move[1]/3
		bl = x*3+y
		self.hv[x][y] = self.heuristic(board, bl, flag)/100.00
		cell = self.balphabeta(board, block, flag, flag, 0, -1000, 1000, old_move)
		print cell, flag
		return cell

	def eval_board(self):
		overall_sum = 0
		#horizontal
		#print type(self.hv[0])
		lsum = 0
		for i in range(3):
			rowsum = 0
			for j in range(3):
				rowsum+=self.hv[i][j]
			x = 1
			flag = 0
			if rowsum < 0:
				flag = 1
				rowsum = -rowsum
			while rowsum>0:
				if rowsum>=1:
					lsum+=1*(x-(x/10))
				else:
					lsum+=rowsum*(x-(x/10))
				x*=10
				rowsum-=1
			if flag == 1:
				lsum = -lsum
			overall_sum += lsum
		
		#vertical
		lsum = 0
		for i in range(3):
			colsum = 0
			for j in range(3):
				colsum+=self.hv[j][i]
			x = 1
			flag = 0
			if colsum < 0:
				flag = 1
				colsum = -colsum
			while colsum>0:
				if colsum>=1:
					lsum+=1*(x-(x/10))
				else:
					lsum+=colsum*(x-(x/10))
				x*=10
				colsum-=1
			if flag == 1:
				lsum = -lsum
			overall_sum += lsum

		#diagonal
		diasum=0
		diasum += self.hv[0][0]
		diasum += self.hv[1][1]
		diasum += self.hv[2][2]
		x = 1
		flag = 0
		if diasum < 0:
			flag = 1
			diasum = -diasum
		lsum = 0
		while diasum>0:
			if diasum>=1:
				lsum+=1*(x-(x/10))
			else:
				lsum+=diasum*(x-(x/10))
			x*=10
			diasum-=1
		if flag == 1:
			lsum = -lsum
		overall_sum += lsum



		diasum=0
		diasum += self.hv[2][0]
		diasum += self.hv[1][1]
		diasum += self.hv[0][2]
		x = 1
		flag = 0
		if diasum < 0:
			flag = 1
			diasum = -diasum
		lsum = 0
		while diasum>0:
			if diasum>=1:
				lsum+=1*(x-(x/10))
			else:
				lsum+=diasum*(x-(x/10))
			x*=10
			diasum-=1
		if flag == 1:
			lsum = -lsum
		overall_sum += lsum

		# for i in range(3):
		# 	for j in range(3):
		# 		print self.hv[i][j],
		# 	print 
		# print overall_sum

		return overall_sum

	def balphabeta(self, board, block, flag, turn, depth, a, b, old_move):
		if depth == 4:
			return self.eval_board()
			#return random.randrange(200) - 100

		if turn == 'x':
			oturn = 'o'
		else:
			oturn = 'x'
		valid_blocks = self.blocks_allowed(old_move, block)
		tboard = [row[:] for row in board]
		tblock = block[:]
		if len(valid_blocks) == 0:
			for i in range(9):
				if block[i] == '-':
					valid_blocks.append(i)
		
		#print cells
		i = -1
		for bl in valid_blocks:
			i+=1
			if a > b:
				return util
			x = bl/3
			y = bl%3
			mv = self.alphabeta(tboard, bl, turn, turn, 0, -1000, 1000)
			ac = self.hv[x][y]
			if type(mv) is int:
				print mv, bl, "skdfjls"
			tboard[mv[0]][mv[1]] = turn
			self.hv[x][y] = self.heuristic(tboard, bl, flag)/100.00
			if self.hv[x][y] == 1:
				tblock[bl] = turn
				if depth == 0:
					return mv
				return (self.max_depth - depth + 1)*100
			elif self.hv[x][y] == -1:
				tblock[bl] = oturn 
				return (self.max_depth - depth + 1)*-100
			h = self.eval_board()
			if h > 50:
				self.hv[x][y] = ac
				tboard[mv[0]][mv[1]] = "-"
				if depth == 0:
					#print "okay"
					return mv
				return (self.max_depth - depth + 1)*100
			elif h < -50:
				self.hv[x][y] = ac
				tboard[mv[0]][mv[1]] = "-"
				if depth == 0:
					#print "okay1"
					pass
				else:
					return (self.max_depth - depth + 1)*-100
			if self.hv[x][y] == 0:
				m = (bl/3)*3
				n = (bl%3)*3
				count = 0
				for p in xrange(m, m+3):
					for q in xrange(n, n+3):
						if tboard[p][q] == '-':
							count += 1
				if count == 0:
					tblock[bl] = "D" 
			v = self.balphabeta(tboard, tblock, flag, oturn, depth+1, a, b, mv)
			self.hv[x][y] = ac
			tboard[mv[0]][mv[1]] = '-'
			if i == 0:
				util = v
			if turn == flag:
				if v > a:
					a = v
					if depth == 0:
						move = mv
				if v > util:
					util = v
			else:
				if v < b:
					b = v
				if v < util:
					util = v
		if depth == 0:
			return move
		return util

	def heuristic(self, board,block_number,player):
		x_start = (block_number/3)*3
		y_start = (block_number%3)*3
		heuristic_value = 0
		# for i in range(3):
		# 	for j in range(3):
		# 		board[x_start+i][y_start+j]=raw_input()
		
		# for i in range(3):
		# 	for j in range(3):
		# 		print board[x_start+i][y_start+j],
		# 	print "\n"

		#horizontal check
		for i in range(3):
			x = x_start + i
			y = y_start
			count_of_empty_cells = 0
			for j in range(3):
				y = y_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start + i
			y = y_start 
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1]):
					return 100
				elif board[x][y]!=player and (board[x][y]==board[x][y+1] and board[x][y+2]==board[x][y+1]):
					return -100
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x][y+1] and board[x][y]==player) or (board[x][y+1]==board[x][y+2] and board[x][y+1]==player) or (board[x][y]==board[x][y+2] and board[x][y]==player) :
					heuristic_value+=10
				elif (board[x][y]==board[x][y+1] and board[x][y]!=player) or (board[x][y+1]==board[x][y+2] and board[x][y+1]!=player) or (board[x][y]==board[x][y+2] and board[x][y]!=player): 
					heuristic_value-=10
			elif count_of_empty_cells==2:
				if board[x][y]==player or board[x][y+1]==player or board[x][y+2]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1	
		#print heuristic_value,"horizontal"
		#vertical check						
		for i in range(3):
			x = x_start
			y = y_start + i
			count_of_empty_cells = 0
			for j in range(3):
				x = x_start + j
				if board[x][y]=='-':
					count_of_empty_cells+=1
			x = x_start
			y = y_start + i
			if count_of_empty_cells==0:
				if board[x][y]==player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y]):
					return 100
				elif board[x][y]!=player and (board[x][y]==board[x+1][y] and board[x+2][y]==board[x+1][y]):
					return -100
			elif count_of_empty_cells==1:
				if (board[x][y]==board[x+1][y] and board[x][y]==player) or (board[x+1][y]==board[x+2][y] and board[x+1][y]==player) or (board[x][y]==board[x+2][y] and board[x][y]==player) :
					heuristic_value+=10
				elif (board[x][y]==board[x+1][y] and board[x][y]!=player) or (board[x+1][y]==board[x+2][y] and board[x+1][y]!=player) or (board[x][y]==board[x+2][y] and board[x][y]!=player): 
					heuristic_value-=10
			elif count_of_empty_cells==2:
				if board[x][y]==player or board[x+1][y]==player or board[x+2][y]==player:
					heuristic_value+=1
				else:
					heuristic_value-=1
		#print heuristic_value,"vertical"
		#diagonal check 1
		count_of_empty_cells = 0
		x = x_start
		y = y_start
		if board[x_start][y_start]=='-':
			count_of_empty_cells+=1
		if board[x_start+1][y_start+1]=='-':
			count_of_empty_cells+=1
		if board[x_start+2][y_start+2]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x_start][y_start]==player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1]):
				return 100
			elif board[x_start][y_start]!=player and (board[x][y]==board[x+1][y+1] and board[x+2][y+2]==board[x+1][y+1]):
				return -100
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x+1][y+1] and board[x][y]==player) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y+1]==player) or (board[x][y]==board[x+2][y+2] and board[x][y]==player) :
				heuristic_value+=10
			elif (board[x][y]==board[x+1][y+1] and board[x][y]!=player) or (board[x+1][y+1]==board[x+2][y+2] and board[x+1][y+1]!=player) or (board[x][y]==board[x+2][y+2] and board[x][y]!=player): 
				heuristic_value-=10
		elif count_of_empty_cells==2:
			if board[x_start][y_start]==player or board[x_start+1][y_start+1]==player or board[x_start+2][y_start+2]==player:
				heuristic_value+=1
			else:
				heuristic_value-=1

		#diagonal check 2
		count_of_empty_cells = 0
		x = x_start+2
		y = y_start
		if board[x][y]=='-':
			count_of_empty_cells+=1
		if board[x-1][y+1]=='-':
			count_of_empty_cells+=1
		if board[x-2][y+2]=='-':
			count_of_empty_cells+=1
		if count_of_empty_cells==0:
			if board[x][y]==player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1]):
				return 100
			elif board[x][y]!=player and (board[x][y]==board[x-1][y+1] and board[x-2][y+2]==board[x-1][y+1]):
				return -100
		elif count_of_empty_cells==1:
			if (board[x][y]==board[x-1][y+1] and board[x][y]==player) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y+1]==player) or (board[x][y]==board[x-2][y+2] and board[x][y]==player) :
				heuristic_value+=10
			elif (board[x][y]==board[x-1][y+1] and board[x][y]!=player) or (board[x-1][y+1]==board[x-2][y+2] and board[x-1][y+1]!=player) or (board[x][y]==board[x-2][y+2] and board[x][y]!=player): 
				heuristic_value-=10
		elif count_of_empty_cells==2:
			if board[x][y]==player or board[x-1][y+1]==player or board[x-2][y+2]==player:
				heuristic_value+=1
			else:
				heuristic_value-=1

		#print "value", heuristic_value
		return heuristic_value

	def alphabeta(self, tboard, bl, flag, turn, depth, a, b):
		if depth == self.max_depth:
			return self.heuristic(tboard, bl, flag)
			#return random.randrange(200) - 100

		if turn == 'x':
			oturn = 'o'
		else:
			oturn = 'x'
		cells = []
		x = (bl/3)*3
		y = (bl%3)*3
		for i in range(3):
			p = x+i
			for j in range(3):
				q = y + j
				if tboard[p][q] == "-":
					cells.append((p,q)) 
				else:
					#print p, q, tboard[p][q]
					pass
		
		#print cells
		for i in range(len(cells)):
			if a > b:
				if depth == 0:
					print "NO!"
				return util
			tboard[cells[i][0]][cells[i][1]] = turn
			h = self.heuristic(tboard, bl, flag)
			if h > 70:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay"
					return cells[i]
				return (self.max_depth - depth + 1)*100
			elif h < -70:
				tboard[cells[i][0]][cells[i][1]] = "-"
				if depth == 0:
					#print "okay1"
					return cells[i]
					pass
				else:
					return (self.max_depth - depth + 1)*-100
			elif h == 0:
				x = (bl/3)*3
				y = (bl%3)*3
				count = 0
				for p in xrange(x, x+3):
					for q in xrange(y, y+3):
						if tboard[p][q] == '-':
							count += 1
				if count == 0:
					if depth == 0:
						return cells[i]
					else:
						return 0
			v = self.alphabeta(tboard, bl, flag, oturn, depth+1, a, b)
			tboard[cells[i][0]][cells[i][1]] = "-"
			if i == 0:
				util = v
			if turn == flag:
				if v > a:
					a = v
					if depth == 0:
						move = cells[i]
				if v > util:
					util = v
			else:
				if v < b:
					b = v
				if v < util:
					util = v
		if cells == []:
			return self.heuristic(tboard, bl, flag)
		if depth == 0:
			return move
		return util


	def  blocks_allowed(self, old_move,block):
		if old_move[0]==-1 and old_move[1]==-1:
			return []
		if old_move[0]%3==0 and old_move[1]%3==0:
			block1 = 1
			block2 = 3
		elif old_move[0]%3==0 and old_move[1]%3==1:
			block1 = 0
			block2 = 2
		elif old_move[0]%3==0 and old_move[1]%3==2:
			block1 = 1
			block2 = 5
		elif old_move[0]%3==1 and old_move[1]%3==0:
			block1 = 0
			block2 = 6
		elif old_move[0]%3==1 and old_move[1]%3==1:
			block1 = 4
		elif old_move[0]%3==1 and old_move[1]%3==2:
			block1 = 2
			block2 = 8
		elif old_move[0]%3==2 and old_move[1]%3==0:
			block1 = 3
			block2 = 7
		elif old_move[0]%3==2 and old_move[1]%3==1:
			block1 = 6
			block2 = 8
		elif old_move[0]%3==2 and old_move[1]%3==2:
			block1 = 5
			block2 = 7

		if block1!=4:
			if block[block1]=='-' and block[block2]=='-':
				return [block1,block2]
			elif block[block1]=='-' and block[block2]!='-':
				return [block1]
			if block[block1]!='-' and block[block2]=='-':
				return [block2]
			if block[block1]!='-' and block[block2]!='-':
				return []
		else:
			if block[4]=='-':
				return [4]
			else:
				return []

	def cells_allowed(self, board, valid_blocks, block):
		cells = []
		for bl in valid_blocks:
			x = (bl/3)*3
			y = (bl%3)*3
			for i in range(3):
				a = x+i
				for j in range(3):
					b = y + j
					if board[a][b] == '-':
						cells.append((a,b))

		if cells == []:
			for bl in range(9):
				if block[bl] == '-':
					x = (bl/3)*3
					y = (bl%3)*3
					for i in range(3):
						a = x+i
						for j in range(3):
							b = y + j
							if board[a][b] == '-':
								cells.append((a,b))

		return cells

def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		sys.exit(1)
	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	return cells
		
# Returns True if move is valid
def check_valid_move(game_board, block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, block_stat)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed, block_stat)
	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		print cells
		return False

def update_lists(game_board, block_stat, move_ret, fl):

	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1

	if flag == 0:
		block_stat[block_no] = 'D'

	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if mflg == 1:
		block_stat[block_no] = fl
	
	return mflg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			if block_stat[i] == '-':
				smfl = 1
				break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE BLOCKS')
	elif status == 'P2':
		return ('P2', 'MORE BLOCKS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list of lists & block_stat is a list of 9 elements indicating if a block has been won.
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	# Player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 12000
	p1_pts=0
	p2_pts=0

	print_lists(game_board, block_stat)

	while(1): # Main game loop
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)

#		try:
#			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
#		except:
#			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
#			print MESSAGE
#			break
		signal.alarm(0)
	
		# Check if list is tampered.
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the returned move is valid
		if not check_valid_move(game_board, block_stat, ret_move_pl1, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break
			

		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl
		# Update the 'game_board' and 'block_stat' move
		p1_pts += update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

        	temp_board_state = game_board[:]
        	temp_block_stat = block_stat[:]

        	signal.signal(signal.SIGALRM, handler)
        	signal.alarm(TIMEALLOWED)

        	try:
           		ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
        	except:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
        	signal.alarm(0)

        	if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
        	if not check_valid_move(game_board, block_stat, ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break

        	print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
        
        	p2_pts += update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

        	# Now check if the last move resulted in a terminal state
        	gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
        	if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			break
        	else:
			old_move = ret_move_pl2
			print_lists(game_board, block_stat)
	
	print WINNER
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = ManualPlayer()
	elif option == '3':
		obj1 = ManualPlayer()
		obj2 = ManualPlayer()
	else:
		print 'Invalid option'
		sys.exit(1)

	num = random.uniform(0,1)
	if num > 0.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
		
	
