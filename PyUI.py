from abc import ABC, abstractmethod
from typing import List

import pygame
from globe import *
import random

# Global pygame variables
keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z, pygame.K_BACKSPACE]


class ViewHandler:
	views = []
	interactable_views = []
	font = None
	screen = None
	clock = None
	TICKS = 60
	
	MIN_TEXT = 10
	
	initial_wait = 20
	wait_per_letter = 3
	initial_wait_counter = 0
	wait_per_letter_counter = 0
	active_key_event = None

	@staticmethod
	def handle_view_events(events):
		ViewHandler.handle_mouse_events(events)
		
		activated_view = None
		for view in ViewHandler.interactable_views:
			if view.active:
				activated_view = view
				break
		
		if activated_view:
			activated_view.handle_events(events)
	
	# Gives all views the mouse events, and removes them from the events list
	@staticmethod
	def handle_mouse_events(events: List[pygame.event.EventType]):
		mouse_events = []
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEWHEEL:  # Any mouse event
				mouse_events.append(event)
				events.remove(event)
		for view in ViewHandler.interactable_views:
			view.handle_events(mouse_events)

	@staticmethod
	def render_views(screen):
		for view in ViewHandler.views:
			if issubclass(view.__class__, AbsTextView):
				view.update()
			view.draw(screen)

	@staticmethod
	def clear_views():
		ViewHandler.views.clear()
		ViewHandler.interactable_views.clear()

	@staticmethod
	def run(process, on_quit):
		process()
		
		ViewHandler.screen.fill(BACKGROUND_COLOR)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				on_quit()
				pygame.quit()
				break
		
		ViewHandler.handle_view_events(events)
		
		ViewHandler.render_views(ViewHandler.screen)
		pygame.display.flip()
		ViewHandler.clock.tick(ViewHandler.TICKS)

	@staticmethod
	def next(view):
		index = ViewHandler.interactable_views.index(view)
		return ViewHandler.interactable_views[(index + 1) % len(ViewHandler.interactable_views)]


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
	def handle_events(self, events):
		pass


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
		self.font_type = "microsoftjhengheimicrosoftjhengheiuilight"
		self.font = pygame.font.SysFont(self.font_type, self.font_size)

	def is_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow

	def set_text(self, text):
		self.text = text

	def get_pixel_size(self):
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		return word_surface.get_size()

	def set_font_size(self, size):
		self.font_size = size
		self.font = pygame.font.SysFont(self.font_type, size)

	def set_font_type(self, font_type):
		self.font_type = font_type
		self.font = pygame.font.SysFont(self.font_type, self.font_size)

	def set_color(self, rgb):
		self.color = rgb

	def draw(self, screen):
		x, y = self.x, self.y
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		screen.blit(word_surface, (x, y))

	def update(self, width, height):
		word_surface = self.font.render(self.text, 0, self.color.to_arr())
		word_width, word_height = word_surface.get_size()

		while word_width * 1.7 <= width and word_height * 1.7 <= height:
			self.set_font_size(self.font_size + 1)
			word_surface = self.font.render(self.text, 0, self.color.to_arr())
			word_width, word_height = word_surface.get_size()

		while (word_width * 1.7 > width or word_height * 1.7 > height) and self.font_size > ViewHandler.MIN_TEXT:
			self.set_font_size(self.font_size - 1)
			word_surface = self.font.render(self.text, 0, self.color.to_arr())
			word_width, word_height = word_surface.get_size()

	def center(self, x, y, width, height):
		text_width, text_height = self.get_pixel_size()
		self.x = x + int((width - text_width) / 2)
		self.y = y + int((height - text_height) / 2)

	def do_rainbow(self):
		r, g, b = self.color.to_arr()
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

	def to_arr(self) -> list:
		return [self.r, self.g, self.b]

	def equals(self, other) -> bool:
		return self.r == other.r and self.g == other.g and self.b == other.b

	def reverted(self):
		return Color(255 - self.r, 255 - self.g, 255 - self.b)

	def is_similar(self, other):
		return abs(self.r - other.r) + abs(self.g - other.g) + abs(self.b - other.b) < 100

	def add(self, amount):
		self.r += amount
		self.r %= 256
		self.g += amount
		self.g %= 256
		self.b += amount
		self.b %= 256
		return self

	def copy(self):
		return Color(self.r, self.g, self.b)

	@staticmethod
	def random_color():
		return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class AbsTextView(View, ABC):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.text = Text(x + 5, y + 5)

		self.on_click_listener = None
		self.on_right_click_listener = None

		self.on_hover_listener = None
		self.on_unhover_listener = None
		self.hover_active = False

		self.obj = pygame.Rect(self.x, self.y, self.w, self.h)
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
			pygame.draw.rect(screen, self.color.to_arr(), self.obj, self.border)
		self.text.draw(screen)
		return self

	def update(self):
		self.text.update(self.w, self.h)
		self.text.center(self.x, self.y, self.w, self.h)

	def handle_events(self, events):
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

	def set_color(self, color):
		self.color = color
		self.text.color = color


class Loader(View, ABC):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.percent = 0
		self.mode = "horizontal"

		self.on_click_listener = None
		self.on_right_click_listener = None
		self.on_hover_listener = None
		self.on_unhover_listener = None
		self.hover_active = False

		self.load_bar = None
		self.color = Color(255, 255, 255)
		self.rainbow = False

	def set_rainbow(self, is_rainbow):
		self.rainbow = is_rainbow

	def load(self, percent):
		pass

	def handle_events(self, events):
		pass

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

	def set_horizontal(self):
		self.mode = "horizontal"

	def set_vertical(self):
		self.mode = "vertical"


class LoadBar(Loader):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		self.frame_rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.load_bar = pygame.Rect(self.x + self.w * 0.05, self.y + self.h / 2, 0.9 * self.w * (self.percent / 100),
		                            self.h / 15)
		self.border = 2
		self.frame = False

	def draw(self, screen):
		if self.frame:
			pygame.draw.rect(screen, self.color.to_arr(), self.frame_rect, self.border)
		pygame.draw.rect(screen, self.color.to_arr(), self.load_bar)
		return self

	def load(self, percent):
		self.percent = percent
		if self.mode == "horizontal":
			self.load_bar = pygame.Rect(self.x + self.w * 0.05, self.y + self.h / 2,
			                            0.9 * self.w * (self.percent / 100), self.h / 15)
		else:
			self.load_bar = pygame.Rect(self.x + self.w / 2, self.y + self.h * 0.05,
			                            self.w / 15, 0.9 * self.h * (self.percent / 100))
		return self

	def set_draw_frame(self, frame):
		self.frame = frame
		return self


class _Point(View):
	def __init__(self, x=0, y=0, radius=2):
		super().__init__(x, y, 6, 6)
		self.radius = radius
		self.color = Color(255, 255, 255)

	def draw(self, screen):
		pygame.draw.circle(screen, self.color.to_arr(), (self.x, self.y), self.radius)
		return self

	def handle_events(self, events):
		pass

	def set_color(self, color):
		self.color = color


class LoadDots(Loader):
	def __init__(self, x, y, w=50, h=50, amount=5, radius=2):
		super().__init__(x, y, w, h)
		self.load_bar = []
		self.amount = amount
		self.current_amount = 0
		self.radius = radius

	def draw(self, screen):
		for point in self.load_bar:
			point.draw(screen)

	def iterate(self):
		self.current_amount += 1
		self.current_amount %= self.amount
		if self.current_amount == 0:
			self.load_bar = []
		else:
			if self.current_amount > 1:
				point = self.load_bar[-1]
				if self.mode == "horizontal":
					point.x += 5
				else:
					point.y += 5
			else:
				point = _Point(self.x, self.y, self.radius)
			self.load_bar.append(point)

	def load(self, percent):
		self.percent = percent
		num = int(self.amount * (percent / 100))
		self.current_amount = num - 1
		self.iterate()


class TextView(AbsTextView):
	def handle_events(self, events):
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
		ViewHandler.interactable_views.append(self)
		self.active = False
		self.original_color = self.color

	def handle_events(self, events):
		if self.on_hover_listener is not None and self.on_unhover_listener is not None:
			if self.obj.collidepoint(pygame.mouse.get_pos()) and not self.hover_active:
				self.on_hover_listener(self)
				self.hover_active = True

			elif self.hover_active:
				self.on_unhover_listener(self)
				self.hover_active = False

		for event in events:
			if event.type == pygame.KEYDOWN:
				if self.active:
					ViewHandler.active_key_event = event
					ViewHandler.initial_wait_counter = 0
					ViewHandler.wait_per_letter_counter = 0
					handle_key(self)
			if event.type == pygame.KEYUP:
				pass
			if event.type == pygame.MOUSEBUTTONDOWN:  # Any button click
				if self.obj.collidepoint(event.pos):
					self.set_active(True)
				else:
					self.set_active(False)

				# TODO: This scroll
				if event.button == 4:  # Scroll Up
					pass
				if event.button == 5:  # Scroll Down
					pass

		if self.active and ViewHandler.active_key_event:
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[ViewHandler.active_key_event.key]:
				if ViewHandler.initial_wait_counter < ViewHandler.initial_wait:
					ViewHandler.initial_wait_counter += 1
				else:
					ViewHandler.wait_per_letter_counter += 1
					if ViewHandler.wait_per_letter_counter == ViewHandler.wait_per_letter:
						handle_key(self)
						ViewHandler.wait_per_letter_counter = 0
			
			else:
				ViewHandler.active_key_event = None
		
		if self.text.rainbow:
			self.text.do_rainbow()

	def set_active(self, flag):
		self.active = flag
		if flag:
			self.text.color = self.original_color.reverted()
		else:
			self.text.color = self.original_color


class Button(AbsTextView):
	def __init__(self, x, y, w=50, h=50):
		super().__init__(x, y, w, h)
		ViewHandler.interactable_views.append(self)
		self.set_draw_frame(True)
		self.active = False
		self.original_color = self.color

	def handle_events(self, events):
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
					if event.key == pygame.K_RETURN:
						self.on_click_listener(self)
					if event.key == pygame.K_TAB:
						self.set_active(False)
						ViewHandler.next(self).set_active(True)

			elif event.type == pygame.MOUSEBUTTONDOWN:  # Any button click
				if self.obj.collidepoint(event.pos):
					if event.button == 1:  # Left click
						self.set_active(True)
						self.on_click_listener(self)
					if event.button == 3:  # Right Click
						self.on_right_click_listener(self)

				else:
					self.set_active(False)

				# TODO: This scroll
				if event.button == 4:  # Scroll Up
					pass
				if event.button == 5:  # Scroll Down
					pass

		if self.text.rainbow:
			self.text.do_rainbow()

	def set_active(self, flag):
		self.active = flag
		if flag:
			self.text.color = self.original_color.reverted()
		else:
			self.text.color = self.original_color


class Screen(View):
	def __init__(self, x=0, y=0, w=50, h=50):
		super().__init__(x, y, w, h)

	def draw(self, screen):
		pass

	def handle_events(self, events):
		pass


def handle_key(view):
	if ViewHandler.active_key_event.key == pygame.K_BACKSPACE:
		view.text.text = view.text.text[:-1]
	elif ViewHandler.active_key_event.key == pygame.K_TAB:
		view.set_active(False)
		ViewHandler.next(view).set_active(True)
	elif ViewHandler.active_key_event.key in keys:
		view.text.text += ViewHandler.active_key_event.unicode
