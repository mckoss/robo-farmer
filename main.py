
from grid import *
from stats import *

#
# Pumpkin Patch
#	
def cultivate_pumpkins(g, water_level):
	def pumpkin_task(x, y, ctx):
		# quick_print("At " + str([x, y]) + ": " + str(get_entity_type()))
		if get_ground_type() != Grounds.Soil:
			till()
		if get_entity_type() == Entities.Pumpkin and can_harvest():
			ctx += 1
		else:
			while get_water() < water_level:
				use_item(Items.Water)
			plant(Entities.Pumpkin)
		return ctx
	
	c = grid_scan(g, pumpkin_task, 0)
	if c == grid_size(g):
		before = num_items(Items.Pumpkin)
		harvest()
		after = num_items(Items.Pumpkin)
		return after - before
		
	return 0
	
def make_pumpkins(goal, grid):
	change_hat(Hats.Pumpkin_Hat)
	pumpkins = 0
	while pumpkins < goal:
		pumpkins += cultivate_pumpkins(grid, 0.25)
	cultivate_pumpkins(grid, 0)
	
	return pumpkins
	
def make_wood(goal, grid):
	def forest_task(x, y, ctx):
		wood_base = num_items(Items.Wood)
		carrot_base = num_items(Items.Carrot)
		if can_harvest():
			harvest()
		if (x + y) % 2 == 0:
			plant(Entities.Tree)
		else:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
		while get_water() < 0.25:
			use_item(Items.Water)
		return (ctx[0] + num_items(Items.Wood) - wood_base,
				ctx[1] + num_items(Items.Carrot) - carrot_base)
	
	change_hat(Hats.Tree_Hat)
	ctx = (0, 0)
	while ctx[0] < goal:
		ctx = grid_scan(grid, forest_task, ctx)
	return ctx

def make_item(goal, item, g, entity, ground_type, water_level):
	items = 0
	def item_task(x, y, ctx):
		if get_ground_type() != ground_type:
			till()
		before = num_items(item)
		if can_harvest():
			harvest()
		if entity != Entities.Grass:
			plant(entity)
		while get_water() < water_level:
			use_item(Items.Water)
		after = num_items(item)
		return ctx + after - before
		
	while items < goal:
		items += grid_scan(g, item_task, 0)

	return items
	
def make_gold(g):
	before = num_items(Items.Gold)
	move_to(add_pos(center(g), (1,1)))
	plant(Entities.Bush)
	substance = width(g) * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	directions = (North, East, South, West)
	idir = 0
	while num_items(Items.Gold) == before:
		for ddir in (1, 0, 3, 2):
			dir = directions[(idir + ddir) % 4]
			if can_move(dir):
				move(dir)
				idir = (idir + ddir) % 4
				break
			
		if get_entity_type() == Entities.Treasure:
			harvest()

	return num_items(Items.Gold) - before
	
def random_dir():
	i = random() * 4 // 1
	return (North, East, South, West)[i]
	
#	
# Farming task functions
#

clear()

target_power = 100
sunflower_grid = [[0, 13], [15, 15]]
pumpkin_grid = [[0, 0], [5, 5]]
forest_grid = [[0, 7], [5, 12]]
cactus_grid = [[7, 0], [15, 8]]
hay_grid = [[6,9], [15, 12]]
maze_size = 16
maze_grid = [[16, 0], [16 + maze_size - 1, maze_size - 1]]

def t1():
	return (("Cactus", make_item(50, Items.Cactus, cactus_grid, Entities.Cactus, Grounds.Soil, 0)),)

def t2():
	return (("Hay", make_item(1000, Items.Hay, hay_grid, Entities.Grass, Grounds.Grassland, 0)),)

def t3():
	r = make_wood(10000, forest_grid)
	return (("Wood", r[0]), ("Carrots", r[1]))

def t4():
	return (("Pumpkins", make_pumpkins(1000, pumpkin_grid)),)
	
def t5():
	if num_items(Items.Power) > target_power:
		return (("Sunflowers", 0),)
	return (("Sunflowers", make_item(50, Items.Power, sunflower_grid, Entities.Sunflower, Grounds.Soil, 0.25)),)
	
def t6():
	return (("Gold", make_gold(maze_grid)),)

all_tasks = (t6, 
	t5, t4, t3, t2, t1
	)

p = 0
while True:
	p = p + 1
	stats = {}
	for task in all_tasks:
		start = get_time()
		r = task()
		end = get_time()
		for prod in r:
			add_stat(stats, prod[0], prod[1], end - start)
	if p % 20 == 1:
		print_stats_heading(stats)
	print_stats(stats)
			
		