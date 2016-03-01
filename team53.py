import sys, random, signal

class Player53(object):
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
			return (7,1)
			#print "first"
		valid_blocks = self.blocks_allowed(old_move, block)
		tboard = [row[:] for row in board]
		bmax = -10
		if len(valid_blocks) == 0:
			for i in range(9):
				if block[i] == '-':
					valid_blocks.append(i)
		for bl in valid_blocks:
			x = bl/3
			y = bl%3
			mv = self.alphabeta(tboard, bl, flag, flag, 0, -1000, 1000)
			a = self.hv[x][y]
			tboard[mv[0]][mv[1]] = flag
			self.hv[x][y] = self.heuristic(tboard, bl, flag)/100
			bv = self.eval_board()
			if bv > bmax:
				bmax = bv
				cell = mv
			self.hv[x][y] = a
			tboard[mv[0]][mv[1]] = '-'
		#cell = self.alphabeta(tboard, bl, flag, flag, 0, -1000, 1000)
		print cell, flag
		return cell

	def eval_board(self):
		overall_sum = 0
		#horizontal
		#print type(self.hv[0])
		for i in range(3):
			rowsum = 0
			for j in range(3):
				rowsum+=self.hv[i][j]
			x = 1
			while rowsum>0:
				if rowsum>=1:
					overall_sum+=1*(x-(x/10))
				else:
					overall_sum+=rowsum*(x-(x/10))
				x*=10
				rowsum-=1
		
		#vertical
		for i in range(3):
			colsum = 0
			for j in range(3):
				colsum+=self.hv[j][i]
			x = 1
			while colsum>0:
				if colsum>=1:
					overall_sum+=1*(x-(x/10))
				else:
					overall_sum+=colsum*(x-(x/10))
				x*=10
				colsum-=1

		#diagonal
		diasum=0
		diasum += self.hv[0][0]
		diasum += self.hv[1][1]
		diasum += self.hv[2][2]
		x = 1
		while diasum>0:
			if diasum>=1:
				overall_sum+=1*(x-(x/10))
			else:
				overall_sum+=diasum*(x-(x/10))
			x*=10
			diasum-=1



		diasum=0
		diasum += self.hv[2][0]
		diasum += self.hv[1][1]
		diasum += self.hv[0][2]
		x = 1
		while diasum>0:
			if diasum>=1:
				overall_sum+=1*(x-(x/10))
			else:
				overall_sum+=diasum*(x-(x/10))
			x*=10
			diasum-=1

		return overall_sum

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