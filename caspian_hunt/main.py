from settings import *
from sea import Sea
from fish import Fish
from bubble import Bubble
from hook import Hook
from plankton import Planktons
from big_fish import Big_Fishes
from dirt import Dirt
from fish_colony import Fish_Colony
from stones import Stones
from text import Text_Box
from menu_scrn import Menu_Screen
from energy_bar import Energy_Bar
from enum import Enum





class Engine:
	class State(Enum):

		INIT = 1
		PLAYING = 2
		PAUSED = 3
		RESTART = 4
		VICTORY = 5

	def __init__(self) -> None:
		pygame.init()
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("times new roman", 20)

		self.display = pygame.display.set_mode((WIDTH, HEIGHT), 
			pygame.DOUBLEBUF | pygame.HWSURFACE)
		pygame.display.set_caption("caspian sea")

		self.surface = pygame.Surface((RES_WIDTH, RES_HEIGHT)).convert()
		self.state = Engine.State.INIT

		self.sea = Sea(self)
		self.fish_colony = Fish_Colony(self)
		self.dirt = Dirt(self)
		self.stones = Stones(self)
		self.fish = Fish(self)
		self.hook = Hook(self)
		self.planktons = Planktons(self)
		self.big_fishes = Big_Fishes(self)
		self.front_bubble = Bubble(self)
		self.text_box = Text_Box(self)
		self.menu_scrn = Menu_Screen(self)
		self.energy_bar = Energy_Bar(self)

	@property
	def keys(self):
		return pygame.key.get_pressed()

	def get_surface(self, surf):
		surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
		return surf


			
	def draw(self) -> None:
		
		if self.state == Engine.State.INIT:
			self.sea.draw()
			self.fish_colony.draw()
			self.dirt.draw()
			self.stones.draw()
			self.fish.draw()
			self.hook.draw()
			self.planktons.draw()
			self.big_fishes.draw()
			self.front_bubble.draw()
			self.text_box.draw()
			self.energy_bar.draw()

		if self.state == Engine.State.PLAYING:
			self.sea.draw()
			self.fish_colony.draw()
			self.dirt.draw()
			self.stones.draw()
			self.fish.draw()
			self.hook.draw()
			self.planktons.draw()
			self.big_fishes.draw()
			self.front_bubble.draw()
			self.energy_bar.draw()

		if self.state == Engine.State.PAUSED:
			self.sea.draw()
			self.fish_colony.draw()
			self.dirt.draw()
			self.stones.draw()
			self.fish.draw()
			self.hook.draw()
			self.planktons.draw()
			self.big_fishes.draw()
			self.front_bubble.draw()
			self.menu_scrn.draw()

		if self.state == Engine.State.RESTART:
			self.sea.draw()
			self.fish_colony.draw()
			self.dirt.draw()
			self.stones.draw()
			self.fish.draw()
			self.hook.draw()
			self.planktons.draw()
			self.big_fishes.draw()
			self.front_bubble.draw()
			self.menu_scrn.draw()

		if self.state == Engine.State.VICTORY:
			self.sea.draw()
			self.fish_colony.draw()
			self.dirt.draw()
			self.stones.draw()
			self.fish.draw()
			self.hook.draw()
			self.planktons.draw()
			self.big_fishes.draw()
			self.front_bubble.draw()
			self.menu_scrn.draw()


	def event(self) -> None:

		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_RETURN:
					self.__init__()
				if e.key == pygame.K_ESCAPE:
					if self.state == Engine.State.PLAYING:
						self.state = Engine.State.PAUSED

					elif self.state == Engine.State.PAUSED:
						self.state = Engine.State.PLAYING

				if e.key == pygame.K_f:
					if self.state == Engine.State.RESTART:
						self.__init__()

					elif self.state == Engine.State.VICTORY:
						self.__init__()

	def update(self) -> None:

		self.state_manager()


	def state_manager(self):

		if self.state == Engine.State.INIT:
			self.sea.update()
			self.stones.update()
			self.text_box.update()

		if self.state == Engine.State.PLAYING:
			pygame.display.set_caption(str(self.clock.get_fps()))
			self.sea.update()
			self.fish_colony.update()
			self.dirt.update()
			self.stones.update()
			self.fish.update()
			self.hook.update()
			self.planktons.update()
			self.big_fishes.update()
			self.front_bubble.update()
			self.energy_bar.update()

		if self.state == Engine.State.PAUSED:
			self.menu_scrn.update()

		if self.state == Engine.State.RESTART:
			self.menu_scrn.update()

		if self.state == Engine.State.VICTORY:
			self.menu_scrn.update()
			

		

	def process(self) -> None:
		
		self.surface.fill("black")
		self.draw()
		self.display.blit(self.get_surface(self.surface), vec2(0))
		self.event()
		self.update()
		pygame.display.update()


if __name__ == "__main__":
	engine = Engine()
	while True:
		engine.process()
		engine.clock.tick()