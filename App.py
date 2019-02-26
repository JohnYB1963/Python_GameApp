from pygame.locals import *
import pygame
from Player import Player
from Maze import Maze
from Enemy import Enemy
import time
import _thread
import random

class App(object):
    windowWidth = 1275
    windowHeight = 500
    player = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self._coin_surf = None
        self._enemy_surf = None
        self.player = Player()
        self.positionLyst = []
        self.maze = Maze("maze3.maz")
        self.e1 = Enemy(1)
        self.e2 = Enemy(2)
        self.e3 = Enemy(3)
        self.e4 = Enemy(4)
        self._startTime = time.time()

    def handleStartEnemyV3(self, e, x, y, z):
        validstart = False
        while not validstart:
            e.findStartLocation()
            if self.maze.mz[int(e.y / 20)][int(e.x / 20)] == " " or self.maze.mz[int(e.y / 20)][int(e.x / 20)] == "X":
                validstart = True
            else:
                e.findStartLocation()

        e.beginPathFinding(self.maze)

        return

    def getDirectionY(self, direction, y):
        if direction == "up":
            y -= 20
            return y
        elif direction == "down":
            y += 20
            return y

    def getDirectionX(self, direction, x):
        if direction == "left":
            x -= 20
            return x
        elif direction == "right":
            x += 20
            return x

    def getInverse(self, direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"

    def on_Death(self):
        self.player._alive = False
        self._running = False

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.pointDisplay = self.myFont.render("Player score: " + str(self.player.totalScore), 1, (255, 255, 255))
        self._elapsedTime = time.time() - self._startTime
        self._timeDisplay = self.myFont.render("Time:" + str(round(self._elapsedTime, 2)), 1, (255, 255, 255))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf, self._coin_surf)
        self._display_surf.blit(self._enemy_surf, (self.e1.x, self.e1.y))
        #self._display_surf.blit(self._enemy_surf, (self.e2.x, self.e2.y))
        #self._display_surf.blit(self._enemy_surf, (self.e3.x, self.e3.y))
        #self._display_surf.blit(self._enemy_surf, (self.e4.x, self.e4.y))
        self._display_surf.blit(self.pointDisplay, (75, 450))
        self._display_surf.blit(self._timeDisplay, (400, 450))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def eat(self):
        if self.maze.mz[int(self.player.y / 20)][int(self.player.x / 20)] == " ":
            self.player.totalScore += 1
            self.maze.mz[int(self.player.y / 20)][int(self.player.x / 20)] = "X"
            self.on_render()

    def on_init(self):
        pygame.init()
        self.myFont = pygame.font.SysFont("Times New Roman", 24)
        self._myFont2 = pygame.font.SysFont("Times New Roman", 34)
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption("UnderGround - ThunderGround")
        self._running = True
        self.pointDisplay = self.myFont.render("Player score: " + str(self.player.totalScore), 1, (255, 255, 255))
        self._image_surf = pygame.image.load("player2.png").convert()
        self._block_surf = pygame.image.load("block2.png").convert()
        self._coin_surf = pygame.image.load("coin2.png").convert()
        self._enemy_surf = pygame.image.load("enemy2.png").convert()
        _thread.start_new_thread(self.handleStartEnemyV3, (self.e1, 1, 2, 3))
        #_thread.start_new_thread(self.handleStartEnemyV3, (self.e2, 1, 2, 3))
        #_thread.start_new_thread(self.handleStartEnemyV3, (self.e3, 1, 2, 3))
        #_thread.start_new_thread(self.handleStartEnemyV3, (self.e4, 1, 2, 3))


    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                if not self.maze.mz[int(self.player.y / 20)][(int(self.player.x / 20)) + 1] == "*":
                    self.player.moveRightI()
                    self.eat()

            if (keys[K_LEFT]):
                if not self.maze.mz[int(self.player.y / 20)][(int(self.player.x / 20)) - 1] == "*":
                    self.player.moveLeftI()
                    self.eat()

            if (keys[K_UP]):
                if not self.maze.mz[int(self.player.y / 20) - 1][(int(self.player.x / 20))] == "*":
                    self.player.moveUpI()
                    self.eat()

            if (keys[K_DOWN]):
                if not self.maze.mz[int(self.player.y / 20) + 1][(int(self.player.x / 20))] == "*":
                    self.player.moveDownI()
                    self.eat()

            time.sleep(0.05)

            if (keys[K_ESCAPE]):
                self._running = False
                self.e1.kill = True
                self.e2.kill = True
                self.e3.kill = True
                self.e4.kill = True


            self.on_loop()
            self.on_render()

        if self.player._alive == False:
            self._hs = open("highscores", "w")
            self._hsString = "Score: " + str(self.player.totalScore) + " Time: " + str(
                round(self._elapsedTime, 2)) + "\n"
            self._hs.write(str(self._hsString) + "\n")
            self._display_surf.fill((0, 0, 0))
            displayString = "You have Died.\n" + "Score: " + str(self.player.totalScore) + "Time: " + str(
                round(self._elapsedTime, 2)) + "\n"
            deathDisplay = self.myFont.render(displayString, 1, (255, 255, 255))
            self._display_surf.blit(deathDisplay, (550, 75))
            pygame.display.flip()
            time.sleep(1)

        self.on_cleanup()
