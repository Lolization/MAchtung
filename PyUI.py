from abc import ABC, abstractmethod
import pygame
from globe import *


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
			if issubclass(view.__class__, AbsTextView):
				view.update()
			view.draw(screen)

	@staticmethod
	def clear_views():
		ViewHandler.views.clear()


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
	def __init__(self, x=0, y=0, w=50, h=50):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		ViewHandler.views.append(self)

	def set_x(self, x):
		self.x = x
		return self

	def set_y(self, y):
		self.y = y
		return self

	def set_width(self, w):
		self.w = w
		return self

	def set_height(self, h):
		self.h = h
		return self

	@abstractmethod
	def draw(self, screen):
		pass

	@abstractmethod
	def handle_events(self, pygame, events):
		pass


class AbsTextView(View, ABC):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.text = Text(x + 5, y + 5)

		self.on_click_listener = None
		self.on_right_click_listener = None

		self.on_hover_listener = None
		self.on_unhover_listener = None
		self.hover_active = False

		self.obj = ViewHandler.pygame.Rect(self.x, self.y, self.w, self.h)
		self.border = 2
		self.color = Color(255, 255, 255)
		self.rainbow = False
		self.frame = False

		self.text.rainbow = self.rainbow

	def set_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow
		self.text.rainbow = is_rainbow
		return self

	def draw(self, screen):
		if self.frame:
			ViewHandler.pygame.draw.rect(screen, self.color.to_arr(), self.obj, self.border)
		self.text.draw(screen)
		return self

	def update(self):
		self.text.update(self.w, self.h)
		self.text.center(self.x, self.y, self.w, self.h)

	def handle_events(self, pygame, events):
		pass

	def set_text(self, text):
		self.text.set_text(text)
		return self

	def set_font_size(self, size):
		self.text.set_font_size(size)
		return self

	def set_font_type(self, font):
		self.text.set_font_type(font)

	def set_on_click_listener(self, listener):
		self.on_click_listener = listener
		return self

	def set_on_right_click_listener(self, listener):
		self.on_right_click_listener = listener
		return self

	def set_on_hover_listener(self, listener):
		self.on_hover_listener = listener
		return self

	def set_on_unhover_listener(self, listener):
		self.on_unhover_listener = listener
		return self

	def set_draw_frame(self, frame):
		self.frame = frame
		return self


class Text:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		self.w = 50
		self.h = 50

		self.active = False
		self.text = "Text"
		self.length = len(self.text)
		self.color = Color(255, 255, 255)
		self.rainbow = False
		self.font_size = FONT_SIZE
		self.font_type = "Courier New"
		self.font = ViewHandler.pygame.font.SysFont(self.font_type, self.font_size)

	def is_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow

	def set_text(self, text):
		self.text = text

	def get_pixel_size(self):
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		return word_surface.get_size()

	def set_font_size(self, size):
		self.font_size = size
		self.font = ViewHandler.pygame.font.SysFont(self.font_type, size)

	def set_font_type(self, type):
		self.font_type = type
		self.font = ViewHandler.pygame.font.SysFont(self.font_type, self.font_size)

	def set_color(self, rgb):
		self.color = rgb

	def draw(self, screen):
		x, y = self.x, self.y
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		screen.blit(word_surface, (x, y))

	def update(self, width, height):
		self.set_font_size(FONT_SIZE)
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		word_width, word_height = word_surface.get_size()
		while word_width * 1.7 > width or word_height * 1.7 > height:
			self.set_font_size(self.font_size - 1)
			word_surface = self.font.render(self.text, 0, self.color.to_arr())
			word_width, word_height = word_surface.get_size()

	def center(self, x, y, width, height):
		text_width, text_height = self.get_pixel_size()
		self.x = x + int((width - text_width) / 2)
		self.y = y + int((height - text_height) / 2)

	def do_rainbow(self):
		r, g, b = self.color.to_arr()
		print(r, g, b)
		if r == 255 and b > 0:
			b -= 1
		elif r == 255 and g < 255:
			g += 1
		elif g == 255 and 0 < r:
			r -= 1
		elif g == 255 and b < 255:
			b += 1
		elif b == 255 and 0 < g:
			g -= 1
		elif b == 255 and r < 255:
			r += 1

		self.color = Color(r, g, b)


class TextView(AbsTextView):
	def handle_events(self, pygame, events):
		if self.on_hover_listener is not None and self.on_unhover_listener is not None:
			if self.obj.collidepoint(pygame.mouse.get_pos()) and not self.hover_active:
				self.on_hover_listener(self)
				self.hover_active = True

			elif self.hover_active:
				self.on_unhover_listener(self)
				self.hover_active = False


class EditText(AbsTextView):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.active = False

	def handle_events(self, pygame, events):
		if self.on_hover_listener is not None and self.on_unhover_listener is not None:
			if self.obj.collidepoint(pygame.mouse.get_pos()):
				self.on_hover_listener(self)
				self.hover_active = True

			elif self.hover_active:
				self.on_unhover_listener(self)
				self.hover_active = False

		for event in events:
			if event.type == pygame.KEYDOWN:
				if self.active:
					if event.key == pygame.K_BACKSPACE:
						self.text.text = self.text.text[:-1]
					else:
						self.text.text += event.unicode
			if event.type == pygame.MOUSEBUTTONDOWN:  # Any button click
				if self.obj.collidepoint(event.pos):
					self.active = True

				else:
					self.active = False

				# TODO: This scroll
				if event.button == 4:  # Scroll Up
					pass
				if event.button == 5:  # Scroll Down
					pass

		if self.text.rainbow:
			self.text.do_rainbow()


class Button(AbsTextView):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.set_draw_frame(True)

	def handle_events(self, pygame, events):
		if self.on_hover_listener is not None and self.on_unhover_listener is not None:
			if self.obj.collidepoint(pygame.mouse.get_pos()):
				self.on_hover_listener(self)
				self.hover_active = True

			elif self.hover_active:
				self.on_unhover_listener(self)
				self.hover_active = False

		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:  # Any button click
				if self.obj.collidepoint(event.pos):
					if event.button == 1:  # Left click
						self.on_click_listener(self)
					if event.button == 3:  # Right Click
						self.on_right_click_listener(self)

				# TODO: This scroll
				if event.button == 4:  # Scroll Up
					pass
				if event.button == 5:  # Scroll Down
					pass

		if self.text.rainbow:
			self.text.do_rainbow()
