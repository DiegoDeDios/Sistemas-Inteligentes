import argparse, random
class Node:
	def __init__(self,pattern,gfunc,move='start'):
		self.pattern = pattern
		self.gfunc = gfunc
		self.move = move
		for (row,i) in zip(pattern,range(3)):
			if 0 in row:
				self.blankloc=[i,row.index(0)]
	def __eq__(self,other):
		if other==None:
			return False

		if isinstance(other,Node)!=True:
			raise TypeError

		for i in range(3):
			for j in range(3):
				if self.pattern[i][j]!=other.pattern[i][j]:
					return False
		return True
	def __getitem__(self,key):
		if isinstance(key,tuple)!=True:
			raise TypeError
		if len(key)!=2:
			raise KeyError

		return self.pattern[key[0]][key[1]]
	def calc_hfunc(self,goal):
		self.hfunc = 0
		for i in range(3):
			for j in range(3):
				# print (i,j)
				if self.pattern[i][j]!=goal.pattern[i][j]:
					self.hfunc+=1
		if self.blankloc != goal.blankloc:
			self.hfunc-=1

		self.ffunc=self.hfunc+self.gfunc

		return self.hfunc,self.gfunc,self.ffunc
	def moveleft(self):
		if self.blankloc[1]==0:
			return None

		left = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
		left[self.blankloc[0]][self.blankloc[1]]=left[self.blankloc[0]][self.blankloc[1]-1]
		left[self.blankloc[0]][self.blankloc[1]-1]=0

		return Node(left,self.gfunc+1,'left')
	def moveright(self):
		if self.blankloc[1]==2:
			return None

		right = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
		right[self.blankloc[0]][self.blankloc[1]]=right[self.blankloc[0]][self.blankloc[1]+1]
		right[self.blankloc[0]][self.blankloc[1]+1]=0

		return Node(right,self.gfunc+1,'right')
	def moveup(self):
		if self.blankloc[0]==0:
			return None

		up = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
		up[self.blankloc[0]][self.blankloc[1]]=up[self.blankloc[0]-1][self.blankloc[1]]
		up[self.blankloc[0]-1][self.blankloc[1]]=0

		return Node(up,self.gfunc+1,'up')
	def movedown(self):
		if self.blankloc[0]==2:
			return None

		down = [[self.pattern[i][j] for j in range(3)]for i in range(3)]
		down[self.blankloc[0]][self.blankloc[1]]=down[self.blankloc[0]+1][self.blankloc[1]]
		down[self.blankloc[0]+1][self.blankloc[1]]=0

		return Node(down,self.gfunc+1,'down')
	def moveall(self,game):
		left = self.moveleft()
		left = None if game.isclosed(left) else left
		right = self.moveright()
		right = None if game.isclosed(right) else right
		up = self.moveup()
		up = None if game.isclosed(up) else up
		down = self.movedown()
		down = None if game.isclosed(down) else down

		game.closeNode(self)
		game.openNode(left)
		game.openNode(right)
		game.openNode(up)
		game.openNode(down)
		
		return left,right,up,down

	def print(self):
		print(self.move+str(self.gfunc))
		print(self.pattern[0])
		print(self.pattern[1])
		print(self.pattern[2])
		

class Game:
	def __init__(self,start,goal):    
		self.start = start
		self.goal = goal
		self.open = {}
		self.closed = {}
		_,_,ffunc = self.start.calc_hfunc(self.goal)
		self.open[ffunc] = [start]

	def isclosed(self,node):
		if node==None:			
			return True

		hfunc,_,_ = node.calc_hfunc(self.goal)

		if hfunc in self.closed:
			for x in self.closed[hfunc]:
				if x==node:
					return True

		return False

	def closeNode(self,node):
		if node==None:	
			return

		hfunc,_,ffunc= node.calc_hfunc(self.goal)
		self.open[ffunc].remove(node)	
		if len(self.open[ffunc])==0:
			del self.open[ffunc]		

		if hfunc in self.closed:
			self.closed[hfunc].append(node)
		else:
			self.closed[hfunc] = [node]

		return
	def openNode(self,node):
		if node==None:
			return

		_,_,ffunc = node.calc_hfunc(self.goal)
		if ffunc in self.open:
			self.open[ffunc].append(node)
		else:
			self.open[ffunc] = [node]

		return

	def solve(self):

		presentNode = None

		while(presentNode!=self.goal):
			i=0
			while i not in self.open:
				i+=1							
			presentNode = self.open[i][-1]		
			presentNode.moveall(self)			
		while presentNode.move!='start':
			presentNode.print()
			if presentNode.move == 'up':
				presentNode = presentNode.movedown()
			elif presentNode.move == 'down':
				presentNode = presentNode.moveup()
			elif presentNode.move == 'right':
				presentNode = presentNode.moveleft()
			elif presentNode.move == 'left':
				presentNode = presentNode.moveright()
			hfunc,_,_ = presentNode.calc_hfunc(self.goal)
			for i in self.closed[hfunc]:
				if i==presentNode:
					presentNode = i

		return

def swap (list, position_a, position_b):
    list[position_a], list[position_b] = list[position_b], list[position_a]

def samples(goal, size):
    inputs = []
    for i in range(0, 100):
        new_puzzle = goal.copy()
        for j in range(0, random.randrange(1, 30)):
            move(new_puzzle, random.randrange(4), size, new_puzzle.index(0))
        inputs.append(new_puzzle)
    return inputs


def move(list, move_number, size, position):
    if position % size != 0 and move_number == 0:
        swap(list, position, position - 1)
    if position % size != size - 1 and move_number == 1:
        swap(list, position, position + 1)
    if position > size - 1 and move_number == 2:
        swap(list, position, position - size)
    if position < (len(list) - size) and move_number == 3 :
        swap(list, position, position + size)

if __name__ == '__main__':
	x = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	inputs = samples(x, 3)
	for i in inputs:
		startloc = [i[0:3],i[3:6],i[6:]]
		print("---------Starting state:--------------")
		print(startloc)
		goalloc = [x[0:3],x[3:6],x[6:]]
		start = Node(startloc,0)
		goal = Node(goalloc,0,'goal')
		game = Game(start, goal)
		game.solve() #Solve Game
		print("-----------FINISHED!------------")
