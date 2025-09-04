from settings import *
from light import Light
from enum import Enum




class Tail_Segment:
	def __init__(self, pos, rad):

		self.pos = pos
		self.rad = rad
		self.vel = vec2(0)


class Big_Fish:
	class State(Enum):

		ALIVE = 1
		DEAD = 2
		ATTACHED_TO_FISH = 3
		CAUGHT_TO_FISH_HOOK = 4

	def __init__(self, engine, pos):

		self.engine = engine
		self.tail = [Tail_Segment(pos + vec2(TILE // 2 - 1 * i, 
			0), TILE // 2 - 1 * i) for i in range(4)]
		angle = radians(random.randint(0, 360))
		self.vel = vec2(cos(angle), sin(angle))
		self.speed = 0
		self.light = Light(engine, self.tail[0].pos, self.tail[0].rad * 2, 64, BIG_FISH_COLOR)
		self.color = BIG_FISH_COLOR
		self.alive = True
		self.speed_limit = BIG_FISH_SPEED
		self.state = Big_Fish.State.ALIVE
		self.just_pressed = False


	def draw(self):

		self.draw_body()
		if self.state == Big_Fish.State.ALIVE:
			self.light.draw()


	def update(self):

		self.state_manager()
		self.input_handler()

	def state_manager(self):
		if self.state == Big_Fish.State.ALIVE:
			self.update_position()
			self.update_velocity()
			self.check_collision_with_fish()
			self.light.pos = self.tail[0].pos

		if self.state == Big_Fish.State.DEAD:
			self.get_attached_to_fish()

		if self.state == Big_Fish.State.ATTACHED_TO_FISH:
			self.tail[0].pos = self.engine.fish.tail[0].pos + self.engine.fish.vel_dir * (self.engine.fish.tail[0].rad + self.tail[0].rad)
			self.update_tail(self.engine.fish.speed)
			if self.engine.keys[pygame.K_l] and not self.just_pressed:
				self.state = Big_Fish.State.DEAD
				self.just_pressed = True
			if self.tail[0].pos.distance_to(self.engine.hook.final_pos) <= self.tail[0].rad + self.engine.hook.trap_rad:
				self.state = Big_Fish.State.CAUGHT_TO_FISH_HOOK
				self.engine.hook.state = self.engine.hook.State.UP

		if self.state == Big_Fish.State.CAUGHT_TO_FISH_HOOK:
			self.go_up()

	def go_up(self):
		self.vel = vec2(0, -1) * HOOK_SPEED
		self.tail[0].pos += self.vel
		self.update_tail(self.vel)
		if self.tail[-1].pos.y <= -self.tail[-1].rad:
			self.alive = False

	def get_attached_to_fish(self):
		if self.tail[0].pos.distance_to(self.engine.fish.tail[0].pos) <= self.tail[0].rad + self.engine.fish.tail[0].rad:
			if self.engine.keys[pygame.K_l] and not self.just_pressed:
				if not self.check_if_fish_is_holding_stone():
					self.state = Big_Fish.State.ATTACHED_TO_FISH
				self.just_pressed = True

	def check_if_fish_is_holding_stone(self):
		return [stone for stone in self.engine.stones.list if stone.state == stone.State.GOT_PICKED]

	def input_handler(self):
		if not self.engine.keys[pygame.K_l]:
			self.just_pressed = False

	def draw_body(self):
		[pygame.draw.circle(self.engine.surface, self.color, tail.pos, tail.rad, 3) for tail in self.tail]
		pygame.draw.line(self.engine.surface, self.color, self.tail[0].pos, self.tail[0].pos + self.vel * TILE // 2, 2)

	def update_velocity(self):
		if self.tail[0].pos.x >= RES_WIDTH:
			self.tail[0].pos.x = RES_WIDTH
			self.vel.x *= -1

		if self.tail[0].pos.x <= 0:
			self.tail[0].pos.x = 0
			self.vel.x *= -1

		if self.tail[0].pos.y >= RES_HEIGHT:
			self.tail[0].pos.y = RES_HEIGHT
			self.vel.y *= -1

		if self.tail[0].pos.y <= 0:
			self.tail[0].pos.y = 0
			self.vel.y *= -1


	def update_position(self):
		self.speed += BIG_FISH_ACC
		if self.speed >= self.speed_limit:
			self.speed = self.speed_limit

		self.tail[0].pos += self.vel * self.speed
		self.update_tail(self.speed)

	def update_tail(self, speed):
		for i in range(1, len(self.tail)):
			dist_vec = self.tail[i - 1].pos - self.tail[i].pos
			r = self.tail[i - 1].rad + self.tail[i].rad
			if int(dist_vec.length()) >= r:
				self.tail[i].pos = self.tail[i - 1].pos - dist_vec.normalize() * (self.tail[i].rad + self.tail[i - 1].rad)
				# self.tail[i].vel = dist_vec.normalize() * speed
				# self.tail[i].pos += self.tail[i].vel

	def check_collision_with_fish(self):
		if self.tail[0].pos.distance_to(self.engine.fish.tail[0].pos) <= self.tail[0].rad + self.engine.fish.tail[0].rad:
			self.engine.state = self.engine.State.RESTART




class Big_Fishes:
	def __init__(self, engine):

		self.engine = engine
		self.list = [Big_Fish(engine, vec2(10)), Big_Fish(engine, vec2(150)), Big_Fish(engine, vec2(10, 150)), Big_Fish(engine, vec2(150, 10))]

	def draw(self):

		[big_fish.draw() for big_fish in self.list]


	def update(self):

		[big_fish.update() for big_fish in self.list]
		self.queue_free()
		self.check_fish_population()

	def check_fish_population(self):
		if not self.list:
			self.engine.state = self.engine.State.VICTORY

	def queue_free(self):
		[self.list.remove(big_fish) for big_fish in self.list if not big_fish.alive]