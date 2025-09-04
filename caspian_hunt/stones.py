from settings import *
from enum import Enum




class Stone:
	class State(Enum):

		KINEMATIC = 1
		STATIC = 2
		GOT_PICKED = 3
		THROWN = 4

	def __init__(self, engine, y, color):

		self.engine = engine
		self.pos = vec2(random.randint(0, RES_WIDTH), random.randint(0, RES_HEIGHT))
		self.rad = random.randint(4, 10)
		self.color = color
		self.collided = False
		self.vel = vec2(0, 1) * self.rad * 0.02
		self.state = Stone.State.KINEMATIC
		self.just_pressed = False
		self.deleted = False

	@property
	def rect(self):
		return pygame.Rect(self.pos.x - self.rad, self.pos.y - self.rad, 2 * self.rad, 2 * self.rad)

	def draw(self):
		pygame.draw.circle(self.engine.surface, self.color, self.pos, self.rad)

	def update(self):
		self.state_manager()
		self.check_rad()

	def state_manager(self):
		if self.state == Stone.State.KINEMATIC:
			self.vel = vec2(0, 0.02 * self.rad)
			self.vel.y += 0.02
			self.update_position()

		elif self.state == Stone.State.STATIC:
			if self.pos.distance_to(self.engine.fish.tail[0].pos) <= self.rad + self.engine.fish.tail[0].rad:
				if self.engine.keys[pygame.K_SPACE] and not self.just_pressed:
					if not self.check_if_fish_is_holding_enemy() and self.engine.energy_bar.energy > ENERGY_BAR_WIDTH // 2:
						self.engine.energy_bar.energy -= ENERGY_BAR_WIDTH // 2
						self.state_transition(Stone.State.GOT_PICKED)
					self.just_pressed = True

				if not self.engine.keys[pygame.K_SPACE]:
					self.just_pressed = False


		elif self.state == Stone.State.GOT_PICKED:
			self.pos = self.engine.fish.tail[0].pos + self.engine.fish.vel_dir * (self.rad + self.engine.fish.tail[0].rad)
			if self.engine.keys[pygame.K_SPACE] and not self.just_pressed:
				self.vel = self.engine.fish.vel_dir * 0.1 * self.rad
				self.state_transition(Stone.State.THROWN)
				self.just_pressed = True

			if not self.engine.keys[pygame.K_SPACE]:
				self.just_pressed = False

		elif self.state == Stone.State.THROWN:
			self.pos += self.vel
			self.check_if_out_of_display()
			for fish in self.engine.big_fishes.list:
				for tail in fish.tail:
					if self.pos.distance_to(tail.pos) <= self.rad + tail.rad:
						fish.state = fish.State.DEAD
						self.deleted = True
						self.add_new_stone(self.rad // 3, 1)
						self.add_new_stone(2 * self.rad // 3, -1)

	def check_if_fish_is_holding_enemy(self):
		return [big_fish for big_fish in self.engine.big_fishes.list if big_fish.state == big_fish.State.ATTACHED_TO_FISH]

	def check_if_out_of_display(self):
		if self.pos.x <= -self.rad or self.pos.x >= RES_WIDTH + self.rad or self.pos.y <= -self.rad:
			self.deleted = True

		if self.pos.y >= RES_HEIGHT - self.rad:
			self.pos.y = RES_HEIGHT - self.rad
			self.state = Stone.State.STATIC

	def check_rad(self):
		if self.rad < 4:
			self.deleted = True
						
	def add_new_stone(self, rad, x):
		stone = Stone(self.engine, 0, self.color)
		stone.rad = rad
		stone.pos = vec2(self.pos.x + stone.rad * x, self.pos.y)
		self.engine.stones.list.append(stone)


	def state_transition(self, state):
		self.state = state

	def update_position(self):
		self.pos.y += self.vel.y
		if self.pos.y >= RES_HEIGHT - self.rad:
			self.pos.y = RES_HEIGHT - self.rad
			self.state_transition(Stone.State.STATIC)

	def check_point_collision(self):
		return [stone for stone in self.engine.stones.list if not stone == self and self.pos.distance_to(stone.pos) <= self.rad + stone.rad]





class Stones:
	def __init__(self, engine):

		self.engine = engine
		self.y_offset = RES_HEIGHT - 50
		colors = [c for c in pygame.color.THECOLORS]
		self.list = [Stone(engine, self.y_offset, random.choice(colors)) for i in range(random.randint(12, 18))]
		self.list += [Stone(engine, self.y_offset + 15, random.choice(colors)) for i in range(random.randint(6, 8))]
		

	def draw(self):
		[stone.draw() for stone in self.list]

	def update(self):
		[stone.update() for stone in self.list]
		self.queue_free()
		self.pick_only_one_stone()

	def pick_only_one_stone(self):
		stones = [stone for stone in self.list if stone.state == stone.State.GOT_PICKED]
		stones.sort(key = lambda x : x.pos.distance_to(self.engine.fish.tail[0].pos))
		[stones[i].state_transition(Stone.State.KINEMATIC) for i in range(1, len(stones))]


	def queue_free(self):
		[self.list.remove(stone) for stone in self.list if stone.deleted]