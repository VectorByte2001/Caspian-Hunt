from settings import *




class Energy_Bar:
	def __init__(self, engine):

		self.engine = engine
		self.energy = 0


	def draw(self):

		pygame.draw.rect(self.engine.surface, "dark violet", (ENERGY_BAR_POS.x, ENERGY_BAR_POS.y, self.energy, ENERGY_BAR_HEIGHT), 0, 3)
		pygame.draw.rect(self.engine.surface, FISH_COLOR, (ENERGY_BAR_POS.x, ENERGY_BAR_POS.y, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT), 1, 3)


	def update(self):

		if self.energy >= ENERGY_BAR_WIDTH:
			self.energy = ENERGY_BAR_WIDTH