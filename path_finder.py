import pygame
import math
import sys
from queue import PriorityQueue

#Width of window
WIDTH = 800
#Setting display
WIN = pygame.display.set_mode((WIDTH,WIDTH))

#Displays heading
pygame.display.set_caption("A* Path Finding Algorithm")

#Colour description
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(128,0,128)
ORANGE=(255,165,0)
GREY=(128,128,128)
TURQUOISE=(64,224,208)


class Spot:
	def __init__(self,row,col,width,total_rows):
		self.row=row
		self.col=col 

		#To determine the position (x,y) in the board
		self.x=row*width 
		self.y=col*width 

		#initially all boxes are white
		self.color=WHITE
		self.neighbours=[]
		self.width=width
		self.total_rows=total_rows

	def get_pos(self):
		return self.row,self.col 

	#To check whether a spot is in closed set.
	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color==GREEN

	def is_barrier(self):
		return self.color==BLACK
		
	def is_start(self):
		return self.color==ORANGE

	def is_end(self):
		return self.color==TURQUOISE

	def reset(self):
		self.color=WHITE

	def make_start(self):
		self.color=ORANGE

	def make_closed(self):
		self.color=RED

	def make_open(self):
		self.color=GREEN

	def make_barrier(self):
		self.color=BLACK

	def make_end(self):
		self.color=TURQUOISE

	def make_path(self):
		self.color=PURPLE

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def update_neighbours(self,grid):
		self.neighbours=[]
		#going down from current cell
		if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
			self.neighbours.append(grid[self.row+1][self.col])

		#Going up
		if self.row>0 and not grid[self.row-1][self.col].is_barrier():
			self.neighbours.append(grid[self.row-1][self.col])


		#going right	
		if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
			self.neighbours.append(grid[self.row][self.col+1])


		#going left
		if self.col>0 and not grid[self.row][self.col-1].is_barrier():
			self.neighbours.append(grid[self.row][self.col-1])




		

	def __lt__(self,other):
		return False;
	
#heuristics function
def h(p1,p2):
	x1,y1=p1
	x2,y2=p2
	#Calculating Manhattan distance
	return abs(x1-x2)+abs(y1-y2)



def reconstruct_path(came_from,current,draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw,grid,start,end):
	#keeping track
	count=0

	#insert nodes in priority queue according to the algorithm
	open_set=PriorityQueue()

	#at first 0 in inserted
	open_set.put((0,count,start))

	#The nodes from where we came from, like B->C , A->B
	came_from={}

	#making the entire matrix infinity at first
	g_score={spot:float("inf") for row in grid for spot in row}
	g_score[start]=0

	#f score tells how far away end node is
	f_score={spot:float("inf") for row in grid for spot in row}
	f_score[start]=h(start.get_pos(),end.get_pos())

	#check if an item is in the priority queu
	open_set_hash={start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				return pygame.quit()

		#we need only node
		current=open_set.get()[2]

		#remove lowest f-score
		open_set_hash.remove(current)

		#print the path, as we found the shortest path
		if current == end:
			reconstruct_path(came_from,end,draw)
			end.make_end()
			return True


		for neighbor in current.neighbours:
			temp_g_score=g_score[current]+1

			#found a better path to reach neighbour
			if temp_g_score<g_score[neighbor]:
				came_from[neighbor]=current
				g_score[neighbor]=temp_g_score
				f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
				if neighbor not in open_set_hash:
					count+=1 
					open_set.put((f_score[neighbor],count,neighbor))
					open_set_hash.add(neighbor) 
					neighbor.make_open()

		draw()
		
		if current!=start:
			current.make_closed()

	return False


#crrate the grid
def make_grid(rows,width):
	grid=[]
	#Run two loops and simply append lists
	gap=width//rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot=Spot(i,j,gap,rows)
			grid[i].append(spot)

	return grid

#Create grid lines
def draw_grid(win,rows,width):
	gap=width//rows 
	for i in range(rows):
		#draw horizontal lines

		pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
		for j in range(rows):
		#draw vertical lines
			pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))

def draw(win,grid,rows,width):
	#fill screen
	win.fill(WHITE)

	#draw all spots
	for row in grid:
		for spot in row:
			spot.draw(win)


	draw_grid(win,rows,width)
	pygame.display.update()

#translates mouse position to row column
def get_clicked_pos(pos,rows,width):
	gap=width//rows 
	y,x=pos
	row=y//gap
	col=x//gap
	return row,col

def main(win,width):

	ROWS=50
	grid=make_grid(ROWS,width)

	start=None
	end=None

	run =True 
	started=False 
	while run:
		draw(win,grid,ROWS,width)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				return pygame.quit()

		

			#checks what mouse button we pressed
			if pygame.mouse.get_pressed()[0]: #checks if left mouse button
				pos=pygame.mouse.get_pos()
				#gives the rows and column we clicked on
				row,col=get_clicked_pos(pos,ROWS,width)
				spot=grid[row][col]

				#place the start position
				if not start and spot!=end:
					start=spot 
					start.make_start()

				#place the end position
				elif not end and spot!=start:
					end=spot 
					end.make_end()


				#place the barriers
				elif spot!=end and spot!=start:
					spot.make_barrier()
			 
			#right most button 
			elif pygame.mouse.get_pressed()[2]:
				pos=pygame.mouse.get_pos()
				#gives the rows and column we clicked on
				row,col=get_clicked_pos(pos,ROWS,width)
				spot=grid[row][col]
				spot.reset()
				if spot==start:
					start=None 
				if spot==end:
					end=None 

			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbours(grid)

					algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)

				if event.key==pygame.K_c:
					start=None
					end=None
					grid=make_grid(ROWS,width)
				
				

				 



	#sys.exit(0)
	pygame.quit()


main(WIN,WIDTH)
#sys.exit(0)
#pygame.display.quit()