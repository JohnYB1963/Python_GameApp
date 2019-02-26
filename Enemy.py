import random
import time

class Enemy(object):

    def __init__(self, id):
        self.id = id
        self.x = 1
        self.y = 1
        self.kill = False


    def findStartLocation(self):
        self.x = random.randint(0, 56) * 20
        self.y = random.randint(0, 20) * 20

    def moveGuy(self):
        choice = random.choice(["up", "down", "left", "right"])

        if choice == "up":
            self.y += 1

        if choice == "down":
            self.y -= 1

        if choice == "left":
            self.x -= 1

        if choice == "right":
            self.x += 1

    def checkForOtherPosibility(self, maze):
        #returns the number of posible other positions
        self.numotherpositions = 0
        if not maze.mz[int(self.y / 20) - 1][int(self.x / 20)] == "*":
            self.numotherpositions += 1
        if not maze.mz[int(self.y / 20) + 1][int(self.x / 20)] == "*":
            self.numotherpositions += 1
        if not maze.mz[int(self.y / 20)][int(self.x / 20)-1] == "*":
            self.numotherpositions += 1
        if not maze.mz[int(self.y / 20)][int(self.x / 20)+1] == "*":
            self.numotherpositions += 1
        
        return self.numotherpositions
    
    def moveOneUnitinDirection(self, choice):
        if choice == "up":
            self.y -= 20

        if choice == "down":
            self.y += 20

        if choice == "left":
            self.x -= 20

        if choice == "right":
            self.x += 20

    def checkifBlockinPath(self, choice, maze):
        if choice == "up" and (maze.mz[int(self.y / 20) - 1][int(self.x / 20)] == "*"):
            return True

        if choice == "down" and (maze.mz[int(self.y / 20) + 1][int(self.x / 20)] == "*"):
            return True

        if choice == "left" and (maze.mz[int(self.y / 20)][int(self.x / 20) - 1] == "*"):
            return True

        if choice == "right" and (maze.mz[int(self.y / 20)][int(self.x / 20)+1] == "*"):
            return True


    def beginPathFinding(self, maze):
        
        newchoice = None
        while True:
            #chose a direction to start going
            print("resetting")
            if newchoice is None:
                choice = random.choice(["up", "down", "left", "right"])
            else:
               choice = newchoice

            movinginsingulardirection = True
            while movinginsingulardirection:
                newchoice = None
              
                if self.checkForOtherPosibility(maze) == 3:
                    #newchoice = input("the guy should be at a crossroads. enter your choice of movement")
                    newchoice = random.choice(["up", "down", "left", "right"])
                    print("choice:", newchoice)
                    self.moveOneUnitinDirection(newchoice)
                    break

                #check for a block immediadly in front of current direction
                if self.checkifBlockinPath(choice, maze):
                   
                    break
                
                self.moveOneUnitinDirection(choice)
                

                time.sleep(0.1)

                if self.kill:
                    break
            if self.kill:
                break