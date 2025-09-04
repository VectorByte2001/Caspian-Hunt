from settings import *




class Particle:
	def __init__(self, engine):

		self.engine = engine
		self.pos = vec2(self.r(0, RES_WIDTH), RES_HEIGHT + self.r(0, 100))
		self.rad = self.r(2, 5)
		self.speed = random.uniform(0.03, 0.25)

	def r(self, a, b):
		return random.randint(a, b)

	def draw(self):

		pygame.draw.circle(self.engine.surface, "white", self.pos, self.rad, max(1, self.rad // 10))


	def update(self):

		self.update_position()

	def update_position(self):
		self.pos.y -= self.speed
		if self.pos.y <= -self.rad:
			self.__init__(self.engine)


class Bubble:
	def __init__(self, engine):

		self.engine = engine
		self.particles = [Particle(self.engine) for i in range(15)]

	

	def draw(self):

		[particle.draw() for particle in self.particles]


	def update(self):

		[particle.update() for particle in self.particles]