def grid_size(g):
	return width(g) * height(g)
	
def height(g):
	return g[1][1] - g[0][1] + 1
	
def width(g):
	return g[1][0] - g[0][0] + 1
	
def center(g):
	return floor_pos(scale_pos(add_pos(g[0], g[1]), 1/2))
	
def rel_pos(p, g):
	return sub_pos(p, g[0])
	
def sub_pos(p1, p2):
	return (p1[0] - p2[0], p1[1] - p2[1])
	
def add_pos(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mult_pos(p1, p2):
	return (p1[0] * p2[0], p1[1] * p2[1])
	
def scale_pos(p, scalar):
	return (p[0] * scalar, p[1] * scalar)
	
def floor_pos(p):
	return (p[0]//1, p[1]//1)
	
def get_pos():
	return (get_pos_x(), get_pos_y())

def in_grid(pos, g):
	return pos[0] >= g[0][0] and pos[0] <= g[1][0] and pos[1] >= g[0][1] and pos[1] <= g[1][1]

def grid_scan(g, f, ctx):
	move_to(g[0])
	w = width(g)
	for dy in range(height(g)):
		for dx in range(width(g)):
			if dy % 2 == 0:
				x = dx
			else:
				x = w - dx - 1
			move_to(add_pos(g[0], [x, dy]))
			ctx = f(x, dy, ctx)
	return ctx
	
def visit_until_all(pos_list, f, ctx):
	if len(pos_list)== 0:
		return
		
	pos = get_pos()
	if not pos in pos_list:
		pos = nearest_neighbor(pos, pos_list)
	visit(pos)
	# --here--
		
	while len(pos_list) != 0:
		n = nearest_neighbor(pos, pos_list)
		if n == None:
			break

def move_to(pos):
	dpos = sub_pos(pos, get_pos())
	for dx in range(abs(dpos[0])):
		if dpos[0] < 0:
			move(West)
		else:
			move(East)
	for dy in range(abs(dpos[1])):
		if dpos[1] < 0:
			move(South)
		else:
			move(North)
			
if __name__ == "__main__":
	quick_print(add_pos((1,2), (3,4)))