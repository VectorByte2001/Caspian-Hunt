from settings import *




class Sea:
	def __init__(self, engine):

		self.engine = engine
		self.water_surf = self.get_water_gradient_surf()
		self.timer = 0

	def get_water_gradient_surf(self):
		surf = pygame.Surface((RES_WIDTH, RES_HEIGHT))
		for i in range(RES_HEIGHT // SEA_DELTA_HEIGHT):
			color = (0, 0, 255 - i * (255 // (RES_HEIGHT // SEA_DELTA_HEIGHT)))
			pygame.draw.rect(surf, color, (0, i * SEA_DELTA_HEIGHT, RES_WIDTH, SEA_DELTA_HEIGHT))
		return surf

	def draw(self):

		# self.engine.surface.blit(self.water_surf, vec2(0))
		self.draw_ripple_effect()

	def update(self):

		self.timer += 1

	def draw_ripple_effect(self):
		for i in range(0, RES_WIDTH, SEA_DELTA_HEIGHT):
			y_offset = SEA_WAVE_MAGNITUDE * sin((i + self.timer) / SEA_WAVELENGTH)
			self.engine.surface.blit(self.water_surf, (i, y_offset), (i, 0, SEA_DELTA_HEIGHT, RES_HEIGHT))