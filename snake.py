import pygame
from random import choices
from globe import *
import time

# TODO - Smoother GUI
# TODO - Powers (like in curve fever)
# TODO - Points counter (score)


class Snake:
    def __init__(self, pos, color, speed, alpha, width):
        self.head = Point(pos[0], pos[1], width / 2, color)
        self.body = [self.head]
        self.color = color
        self.alpha = alpha
        self.speed = speed
        self.width = width
        self.degree = 2
        self.gap = False
        self.gap_count = 0
        self.gap_length = self.width * 3
        self.gap_id = 0
        self.gap_marks = []
        self.prob = [GAP_PROB]  # self.prob[0] = prob for gap
        self.prob.append(1 - self.prob[0])

    def draw(self, window):
        t = time.time()
        for index, point in enumerate(self.body):
            if not point.gap:
                point.draw(window)

            if index > 10:
                p = self.body[index - 10]
                if self.is_after_gap(p) or self.is_before_gap(p):
                    p.draw(window)

        self.head.draw(window)
        print("snake drawing time: ", time.time() - t)

    def is_after_gap(self, point):
        index = self.body.index(point)
        if index <= 0:
            return False
        elif not point.gap and self.body[index - 1].gap:
            return True
        return False

    def is_before_gap(self, point):
        index = self.body.index(point)
        if index >= len(self.body) - 1:
            return False
        elif not point.gap and self.body[self.body.index(point) + 1].gap:
            return True
        return False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.alpha += self.degree

        if keys[pygame.K_RIGHT]:
            self.alpha -= self.degree

        head = Point(self.head.x, self.head.y, self.width / 2, self.color)
        head.x += math.cos(degree_to_rad(self.alpha)) * self.speed
        head.y -= math.sin(degree_to_rad(self.alpha)) * self.speed
        self.head = head

        flag = self.gap_count >= self.gap_length
        if not self.gap or flag:
            if flag:
                self.gap_id += 1
            self.head.gap = False
            self.gap_count = 0
            self.gap = False
            has_gap = choices([True, False], self.prob)[0]
            if has_gap:
                self.gap = True
            self.body.append(head)

        else:
            self.head.gap = True
            self.head.gap_id = self.gap_id
            print("in gap: ", self.gap_count)
            self.gap_count += 1
            self.body.append(self.head)

    def lost(self, other_head, window):
        width, height = pygame.display.get_surface().get_size()
        length = len(self.body)
        if other_head.equals(self.head):
            length -= 15
        for i in range(length):
            point = self.body[i]
            if point.collides(other_head):
                if point.gap and (point.gap_id not in self.gap_marks):
                    print('gap_id: ', point.gap_id, ' gaps_mark: ', self.gap_marks)
                    self.draw_gap(point, window)
                    self.gap_marks.append(point.gap_id)
                    return False
                elif point.gap:
                    return False
                else:
                    print("collides")
                    return True
        if self.head.x + self.head.radius >= width:
            print("right wall")
            return True
        if self.head.x - self.head.radius <= 0:
            print("left wall")
            return True
        if self.head.y + self.head.radius >= height:
            print("bottom")
            return True
        if self.head.y - self.head.radius <= 0:
            print("roof")
            return True
        return False

    def add(self, head):
        if self.head.equals(head):
            return
        self.head = head
        if not head.gap:
            self.body.append(head)

    def draw_gap(self, point, window):
        index = self.body.index(point)
        i = index
        while i >= 0:
            point = self.body[i]
            if not point.gap:
                j = i
                while j >= max(0, i): # make it j >= max(0, i - _) for longer painting
                    point = self.body[j]
                    point.draw_gap(window)
                    self.body[j].color = self.body[j].color.reverted()
                    j -= 1
                break
            i -= 1
        i = index
        while i < len(self.body):
            point = self.body[i]
            if not point.gap:
                j = i
                while j <= min(len(self.body) - 1, i):
                    point = self.body[j]
                    point.draw_gap(window)
                    self.body[j].color = self.body[j].color.reverted()
                    j += 1
                break
            i += 1

    def initialize(self, x, y, color, alpha):
        self.color = color
        self.head.x = x
        self.head.y = y
        self.head.color = color
        self.body = [self.head]
        self.alpha = alpha % 360


class Point:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.gap = False
        self.gap_id = -1

    def draw(self, window):
        pygame.draw.circle(window, self.color.to_arr(), (int(self.x), int(self.y)), int(self.radius))

    def collides(self, other):
        dis = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
        if dis <= 1.95 * self.radius:  # 2 * self.radius, although fitting the math logic, seemed to be too much
            print("dis: ", dis, ", radius: ", self.radius)
            return True
        return False

    def equals(self, other):
        if self.x == other.x and self.y == other.y and self.radius == other.radius and self.color.equals(other.color):
            return True
        return False

    def draw_gap(self, window):
        pygame.draw.circle(window, self.color.reverted().to_arr(),
                           (int(self.x), int(self.y)), int(self.radius))
