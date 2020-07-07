from abc import ABC, abstractmethod
import pygame


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


class Color:
	def __init__(self, r, g=None, b=None):
		if isinstance(r, Color):  # r is Color
			self.r = r.r
			self.g = r.g
			self.b = r.b
		else:
			self.r = r
			self.g = g
			self.b = b

	def set_color(self, rgb):
		self.r = rgb.r
		self.g = rgb.g
		self.b = rgb.b
		return self

	def to_arr(self):
		return [self.r, self.g, self.b]


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
		self.color = Color(255, 255, 255)
		self.rainbow = False
		self.font = ViewHandler.pygame.font.SysFont("David", 24)

	def is_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow

	def set_text(self, text):
		self.text = text

	def set_color(self, rgb):
		self.color = rgb

	def draw(self, screen):
		txt_surface = self.font.render(self.text, True, self.color.to_arr())
		screen.blit(txt_surface, (self.x, self.y))

		words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
		space = self.font.size(' ')[0]  # The width of a space.
		max_width, max_height = screen.get_size()
		x, y = self.x, self.y
		for line in words:
			for word in line:
				word_surface = self.font.render(word, 0, self.color.to_arr())
				word_width, word_height = word_surface.get_size()
				if x + word_width >= max_width:
					x = self.x[0]  # Reset the x.
					y += word_height  # Start on new row.
				screen.blit(word_surface, (x, y))
				x += word_width + space
			x = self.x  # Reset the x.
			y += word_height  # Start on new row.


class Button(View):

	def __init__(self, x=0, y=0):
		super().__init__(x, y)

		self.active = False
		self.w = 100

		self.on_click_listener = None
		self.on_right_click_listener = None
		self.on_hover_listener = None

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
			if event.type == pygame.MOUSEBUTTONDOWN:  # Any button click
				if self.obj.collidepoint(event.pos):
					if event.button == 1:  # Left click
						self.on_click_listener(self)
					elif event.button == 3:  # Right Click
						self.on_right_click_listener(self)

				# TODO: This scroll
				if event.button == 4:  # Scroll Up
					pass
				if event.button == 5:  # Scroll Down
					pass

	def set_text(self, text):
		self.text.set_text(text)

	def set_on_click_listener(self, listener):
		self.on_click_listener = listener
		return self

	def set_on_right_click_listener(self, listener):
		self.on_right_click_listener = listener
		return self

	def set_on_hover_listener(self, listener):
		self.on_hover_listener = listener
		return self
