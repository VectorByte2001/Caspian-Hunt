from settings import *
from enum import Enum
from light import Light




class Tail_Segment:
	def __init__(self, pos, rad):

		self.pos = pos
		self.rad = rad
		self.vel = vec2(0)


class Fish:

	class State(Enum):

		NORMAL = 1
		CAUGHT = 2

	def __init__(self, engine):

		self.engine = engine
		self.tail = [Tail_Segment(vec2(RES_WIDTH, RES_HEIGHT) // 2 + vec2(TILE // 2 - 1 * i, 
			0), TILE // 2 - 1 * i) for i in range(4)]
		self.angle = 0
		self.speed = 0
		self.state = Fish.State.NORMAL

	@property
	def vel(self):
		return vec2(cos(radians(self.angle)), sin(radians(self.angle))).normalize() * self.speed

	@property
	def vel_dir(self):
		return vec2(cos(radians(self.angle)), sin(radians(self.angle))).normalize()

	def draw(self):

		self.draw_body()


	def update(self):

		self.state_manager()


	def state_manager(self):
		if self.state == Fish.State.NORMAL:
			self.update_angle()
			self.update_position()
			self.check_collision_with_hook_trap()
			self.keep_position_within_display()

		if self.state == Fish.State.CAUGHT:
			self.go_up()

	def keep_position_within_display(self):
		if self.tail[0].pos.x <= self.tail[0].rad:
			self.tail[0].pos.x = self.tail[0].rad
			self.vel.x = 0
			self.speed = 0.3

		if self.tail[0].pos.x >= RES_WIDTH - self.tail[0].rad:
			self.tail[0].pos.x = RES_WIDTH - self.tail[0].rad
			self.vel.x = 0
			self.speed = 0.3

		if self.tail[0].pos.y <= self.tail[0].rad:
			self.tail[0].pos.y = self.tail[0].rad
			self.vel.y = 0
			self.speed = 0.3

		if self.tail[0].pos.y >= RES_HEIGHT - self.tail[0].rad:
			self.tail[0].pos.y = RES_HEIGHT - self.tail[0].rad
			self.vel.y = 0
			self.speed = 0.3

	def go_up(self):
		vel = vec2(0, -1)
		self.speed = HOOK_SPEED
		self.tail[0].pos += vel * self.speed
		self.update_tail()
		if self.tail[-1].pos.y <= -self.tail[-1].rad:
			self.engine.state = self.engine.State.RESTART


	def draw_body(self):
		[pygame.draw.circle(self.engine.surface, FISH_COLOR, tail.pos, tail.rad, 3) for tail in self.tail]
		pygame.draw.line(self.engine.surface, FISH_COLOR, self.tail[0].pos, self.tail[0].pos + self.vel_dir * TILE // 2, 2)

	def update_angle(self):
		dx = 0
		dx += self.engine.keys[pygame.K_d] - self.engine.keys[pygame.K_a]
		self.angle += dx

	def update_position(self):
		if self.engine.keys[pygame.K_w]:
			self.speed += FISH_ACC
			if self.speed >= FISH_SPEED:
				self.speed = FISH_SPEED

		else:
			self.speed -= FISH_ACC
			if self.speed <= 0:
				self.speed = 0

		self.tail[0].pos += self.vel
		self.update_tail()

	def update_tail(self):
		for i in range(1, len(self.tail)):
			dist_vec = self.tail[i - 1].pos - self.tail[i].pos
			r = self.tail[i - 1].rad + self.tail[i].rad
			if int(dist_vec.length()) == r:
				self.tail[i].vel = dist_vec.normalize() * self.speed
				self.tail[i].pos += self.tail[i].vel

	def check_collision_with_hook_trap(self):
		if self.tail[0].pos.distance_to(self.engine.hook.final_pos) <= self.tail[0].rad + self.engine.hook.trap_rad:
			self.engine.hook.state = self.engine.hook.State.FISH_CAUGHT
			self.state = Fish.State.CAUGHT