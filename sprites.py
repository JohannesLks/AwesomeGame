import pygame as pg
from settings import *
vec = pg.math.Vector2


class Sprite():
    def __init__(self, image, x, y):
        self.image = pg.image.load(image).convert_alpha()
        # print(id(self.image))
        self.rect = self.image.get_rect()
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.rect.topleft = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def events(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)


class RoterF(Sprite):

    def events(self):
        self.acc.x, self.acc.y = 0, 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keystate[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC
        if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

    def update(self):
        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        #self.vel = vec(round(self.vel.x, 2), round(self.vel.y, 2))

        if self.vel.x > MAX_VEL:
            self.vel.x = MAX_VEL
        if self.vel.x < -MAX_VEL:
            self.vel.x = -MAX_VEL
        if self.vel.y > MAX_VEL:
            self.vel.y = MAX_VEL
        if self.vel.y < -MAX_VEL:
            self.vel.y = -MAX_VEL
        #self.pos += self.vel + 0.5 * self.acc
        #self.rect.topleft = self.pos

    def update_pos(self):
        self.pos += self.vel
        self.rect.topleft = self.pos