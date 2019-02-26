class Maze(object):

    def __init__(self, filename):
        self.mz = []

        self._f = open(filename)
        for line in self._f:
            self.mz.append(list(line))

    def draw(self, display_surf, image_surf, coin_surf):
        for j in range(21):
            for i in range(58):
                if self.mz[j][i] == "*":
                    display_surf.blit(image_surf, (i*20, j*20))
                elif self.mz[j][i] == " ":
                    display_surf.blit(coin_surf, (i*20, j*20))