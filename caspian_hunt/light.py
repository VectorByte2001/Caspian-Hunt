from settings import *




class Light:
	def __init__(self, engine, pos, rad, alpha, color):

		self.engine = engine
		self.pos = pos
		self.rad = rad
		self.alpha = alpha
		self.color = color


	def draw(self):

		surf = pygame.Surface(vec2(self.rad * 2), pygame.SRCALPHA)
		pygame.draw.circle(surf, self.color, vec2(self.rad), self.rad)
		surf.set_alpha(self.alpha)
		self.engine.surface.blit(surf, self.pos - vec2(self.rad), special_flags = pygame.BLEND_ADD)


	def update(self):

		...