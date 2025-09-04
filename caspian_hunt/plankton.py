from settings import *
from light import Light




class Plankton:
	def __init__(self, engine):

		self.engine = engine
		self.pos = vec2(self.r(0, RES_WIDTH), self.r(0, RES_HEIGHT))
		self.rad = self.r(4, 10)
		self.collided = False
		self.eaten = False
		self.timer = 0
		self.vel = self.randomize_velocity()
		self.speed = 0.1
		self.light = Light(engine, self.pos, self.rad * 2, 2, PLANKTON_COLOR)


	def r(self, a, b):
		return random.randint(a, b)

	def randomize_velocity(self):
		random_angle = radians(self.r(0, 360))
		return vec2(cos(random_angle), sin(random_angle))

	def draw(self):

		pygame.draw.circle(self.engine.surface, PLANKTON_COLOR, self.pos, self.rad)
		self.light.draw()


	def update(self):

		self.update_position()
		self.update_velocity()
		self.check_collision_with_fish()
		self.update_light()

	def timeout(self):
		now = pygame.time.get_ticks() / 1000
		if now - self.timer > 1:
			self.timer = now
			return True

		else:
			return False

	def update_velocity(self):
		if self.timeout():
			self.vel = self.randomize_velocity()

		if self.collided:
			self.vel = vec2(0)

	def update_position(self):
		self.pos += self.vel * self.speed
		if self.pos.x >= RES_WIDTH + self.rad or self.pos.x <= -self.rad:
			self.pos.x *= -1

		if self.pos.y >= RES_HEIGHT + self.rad or self.pos.y <= -self.rad:
			self.pos.y *= -1

	def check_collision_with_fish(self):
		if self.pos.distance_to(self.engine.fish.tail[0].pos) <= self.rad + self.engine.fish.tail[0].rad:
			self.collided = True

	def update_light(self):
		self.light.pos = self.pos
		self.light.rad = 2 * self.rad
		
		if self.collided:
			self.rad -= 0.1
			if self.rad <= 0:
				if self.engine.energy_bar.energy == ENERGY_BAR_WIDTH:
					self.__init__(self.engine)
				else:
					self.engine.energy_bar.energy += 17
					self.eaten = True





class Planktons:
	def __init__(self, engine):

		self.engine = engine
		self.list = [Plankton(engine) for i in range(15)]


	def draw(self):

		[plankton.draw() for plankton in self.list]


	def update(self):

		[plankton.update() for plankton in self.list]
		self.queue_free()

	def queue_free(self):
		[self.list.remove(plankton) for plankton in self.list if plankton.eaten]
