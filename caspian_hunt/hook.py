from settings import *
from enum import Enum




class Hook:

	class State(Enum):
		UP = 1
		DOWN = 2
		FISH_CAUGHT = 3

	def __init__(self, engine):

		self.engine = engine
		self.pos = vec2(random.randint(0, RES_WIDTH), 0)
		self.length = 0
		self.speed = HOOK_SPEED
		self.trap_rad = 10
		self.state = Hook.State.DOWN

	@property
	def final_pos(self):
		return self.pos + self.length * vec2(0, 1)

	@property
	def rect(self):
		return pygame.Rect(self.final_pos.x - self.trap_rad, self.final_pos.y - self.trap_rad,
			self.trap_rad * 2, self.trap_rad * 2)


	def draw(self):

		pygame.draw.line(self.engine.surface, "gray", self.pos, self.final_pos)
		pygame.draw.circle(self.engine.surface, "red", self.rect.center, self.trap_rad)


	def update(self):

		self.state_manager()

	def state_manager(self):
		if self.state == Hook.State.DOWN:
			self.going_down()

		if self.state == Hook.State.UP:
			self.going_up()

		if self.state == Hook.State.FISH_CAUGHT:
			self.going_up()

	def going_down(self):
		self.length += self.speed
		if self.length > RES_HEIGHT:
			self.state = Hook.State.UP

	def going_up(self):
		self.length -= self.speed
		if self.length < 0:
			self.__init__(self.engine)