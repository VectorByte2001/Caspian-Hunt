from settings import *




class Text_Font:
	def __init__(self, pos, surf):
		
		self.pos = pos
		self.surf = surf

	def draw(self, bg_surf):
		bg_surf.blit(self.surf, self.pos)


class Text_Box:
	def __init__(self, engine):

		self.engine = engine
		self.bg_surf = pygame.Surface((RES_WIDTH, RES_HEIGHT // 3))
		self.bg_surf.set_alpha(255)
		self.text_string = ["press 'E' to continue", "move forward with W, Rotate with   A, S",
		"try to AVOID LIVING ORANGE   FISHES and RED FISH HOOK", "eat the violet planktons to fill           energy bar(its at the topright of         screen)", "with enough energy you can lift one stone with SPACEBAR", "While lifting stone, throw them        with SPACEBAR at the direction       you're facing",
		"you can KNOCK OUT ORANGE       FISH by THROWING STONE     AT THEM", "get near knocked out orange fish       and Press L to grab them", 
		"then get near to the fish hook with      the orange fish to entrap them to      the fish hook", "You can't grab stone and red fish at the same time"]
		self.line_idx = 0
		self.pos = vec2(0, 2 * RES_HEIGHT // 3)
		self.just_pressed = False
		self.text_fonts = [ ]
		self.update_text_fonts()

	def draw(self):

		self.draw_text()
		self.draw_bg()


	def update(self):

		self.bg_surf.fill("black")
		self.update_line_idx()


	def draw_text(self):
		[font.draw(self.bg_surf) for font in self.text_fonts]

	def update_line_idx(self):
		if self.engine.keys[pygame.K_e] and not self.just_pressed:
			self.line_idx += 1
			if self.line_idx <= len(self.text_string) - 1:
				self.update_text_fonts()
			self.just_pressed = True

		if not self.engine.keys[pygame.K_e]:
			self.just_pressed = False

		if self.line_idx > len(self.text_string) - 1:
			self.line_idx = len(self.text_string) - 1
			self.engine.state = self.engine.State.PLAYING

	def update_text_fonts(self):
		self.text_fonts.clear()
		text_surf = [self.engine.font.render(a, "black", "white") for a in self.text_string[self.line_idx]]
		
		for i, char in enumerate(text_surf):
			x, y = 0, 0
			for j in range(0, i):
				x += text_surf[j].get_width()
				if x + text_surf[j].get_width() > RES_WIDTH:
					x = 0
					y += text_surf[j].get_height()
			self.text_fonts.append(Text_Font(vec2(x, y), char))

	def draw_bg(self):
		self.engine.surface.blit(self.bg_surf, self.pos)