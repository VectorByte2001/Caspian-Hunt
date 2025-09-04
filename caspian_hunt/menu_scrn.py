from settings import *




class Menu_Screen:
	def __init__(self, engine):

		self.engine = engine
		self.bg_surf = pygame.Surface((RES_WIDTH, RES_HEIGHT // 3))
		self.text = "PRESS ESC TO CONTINUE"


	def draw(self):

		surf = self.engine.font.render(self.text, "black", "white")
		self.bg_surf.blit(surf, vec2(self.bg_surf.get_size()) // 2 - vec2(surf.get_size()) // 2)
		self.engine.surface.blit(self.bg_surf, vec2(0, RES_HEIGHT // 2))

	def update(self):
		self.bg_surf.fill("black")
		if self.engine.state == self.engine.State.PAUSED:
			self.text = "PRESS ESC TO CONTINUE"

		if self.engine.state == self.engine.State.RESTART:
			self.text = "YOU DIED.PRESS F TO RESTART"

		if self.engine.state == self.engine.State.VICTORY:
			self.text = "YOU WON.PRESS F TO RESTART"