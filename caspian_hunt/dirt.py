from settings import *




class Particle:
	def __init__(self, engine):

		self.engine = engine
		self.pos = vec2(self.r(0, RES_WIDTH), -self.r(0, 200))
		self.rad = self.r(1, 3)
		self.speed = random.uniform(0.02, 0.2)

	def r(self, a, b):
		return random.randint(a, b)

	def draw(self):
		pygame.draw.circle(self.engine.surface, pygame.Color("coral4"), self.pos, self.rad)

	def update(self):
		self.update_position()

	def update_position(self):
		self.pos.y += self.speed
		if self.pos.y >= RES_HEIGHT:
			self.__init__(self.engine)

class Dirt:
	def __init__(self, engine):

		self.engine = engine
		self.list = [Particle(engine) for i in range(20)]


	def draw(self):

		[dirt.draw() for dirt in self.list]


	def update(self):

		[dirt.update() for dirt in self.list]