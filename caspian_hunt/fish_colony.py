from settings import *



class Small_Fish:
	def __init__(self, engine, pos, color, rad):

		self.engine = engine
		self.pos = pos
		self.color = color
		self.rad = rad
		self.rached = False

	def draw(self):
		pygame.draw.circle(self.engine.surface, self.color, self.pos, self.rad)

	def update(self):
		self.pos.x += 0.035
		if self.pos.x > RES_WIDTH + self.rad:
			self.reached = True



class Fish_Colony:
	def __init__(self, engine):

		self.engine = engine
		self.y_offset = 50
		colors = [c for c in pygame.color.THECOLORS]
		self.fishes = [[Small_Fish(engine, vec2(i * 10 + random.randint(0, i * 4), self.y_offset + 10 * j), random.choice(colors), 1) for i in range(random.randint(2, 8))] for j in range(1, 6)]


	def draw(self):

		[[fish.draw() for fish in row] for row in self.fishes]



	def update(self):

		[[fish.update() for fish in row] for row in self.fishes]