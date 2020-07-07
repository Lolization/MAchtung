from abc import ABC, abstractmethod


class ViewHandler:

	views = []
	pygame = None
	font = None

	@staticmethod
	def set_pygame(pygame):
		ViewHandler.pygame = pygame

	@staticmethod
	def handle_view_events(events):
		for view in ViewHandler.views:
			view.handle_events(ViewHandler.pygame, events)

	@staticmethod
	def render_views(screen):
		for view in ViewHandler.views:
			view.draw(screen)


class View(ABC):

	@abstractmethod
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		self.w = 50
		self.h = 50
		ViewHandler.views.append(self)

	@abstractmethod
	def draw(self, screen):
		pass

	@abstractmethod
	def handle_events(self, pygame, events):
		pass


class Text:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		self.w = 50
		self.h = 50

		self.active = False
		self.text = "Button"
		self.r = 255
		self.g = 255
		self.b = 255
		self.rainbow = False
		self.font = ViewHandler.pygame.font.SysFont("David", 24)

	def is_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow

	def set_text(self, text):
		self.text = text

	def set_color(self, rgb):
		self.r, self.g, self.b = rgb

	def draw(self, screen):
		txt_surface = self.font.render(self.text, True, [self.r, self.g, self.b])
		screen.blit(txt_surface, (self.x, self.y))

		words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
		space = self.font.size(' ')[0]  # The width of a space.
		max_width, max_height = screen.get_size()
		x, y = self.x, self.y
		for line in words:
			for word in line:
				word_surface = self.font.render(word, 0, [self.r, self.g, self.b])
				word_width, word_height = word_surface.get_size()
				if x + word_width >= max_width:
					x = self.x[0]  # Reset the x.
					y += word_height  # Start on new row.
				screen.blit(word_surface, (x, y))
				x += word_width + space
			x = self.x  # Reset the x.
			y += word_height  # Start on new row.

	def do_rainbow(self):
		if self.r == 255 and self.b > 0:
			self.b -= 1
		elif self.r == 255 and self.g < 255:
			self.g += 1
		elif self.g == 255 and 0 < self.r:
			self.r -= 1
		elif self.g == 255 and self.b < 255:
			self.b += 1
		elif self.b == 255 and 0 < self.g:
			self.g -= 1
		elif self.b == 255 and self.r < 255:
			self.r += 1


class Button(View):

	def __init__(self, x=0, y=0):
		super().__init__(x, y)

		self.active = False
		self.w = 100
		self.on_click_listener = None
		self.text = Text(x, y)
		self.obj = ViewHandler.pygame.Rect(self.x, self.y, self.w, self.h)
		self.border = 2
		self.r = 255
		self.g = 255
		self.b = 255
		self.rainbow = False

		self.text.rainbow = self.rainbow

	def is_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow
		self.text.rainbow = is_rainbow

	def draw(self, screen):
		ViewHandler.pygame.draw.rect(screen, [self.r, self.g, self.b], self.obj, self.border)
		self.text.draw(screen)

	def handle_events(self, pygame, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:

				# If the user clicked on the view.
				if self.obj.collidepoint(event.pos):
					self.on_click_listener(self)

		if self.rainbow:
			self.do_rainbow()

			if self.text.rainbow:
				self.text.do_rainbow()

	def set_text(self, text):
		self.text.set_text(text)

	def do_rainbow(self):
		if self.r == 255 and self.b > 0:
			self.b -= 1
		elif self.r == 255 and self.g < 255:
			self.g += 1
		elif self.g == 255 and 0 < self.r:
			self.r -= 1
		elif self.g == 255 and self.b < 255:
			self.b += 1
		elif self.b == 255 and 0 < self.g:
			self.g -= 1
		elif self.b == 255 and self.r < 255:
			self.r += 1

	def set_on_click_listener(self, listener):
		self.on_click_listener = listener
		return self
