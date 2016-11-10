import random
import collections

import pygame

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
SPEED = 15
CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

Coords = collections.namedtuple('Coords', ('x', 'y'))

UP = Coords(x=0, y=-1)
DOWN = Coords(x=0, y=1)
LEFT = Coords(x=-1, y=0)
RIGHT = Coords(x=1, y=0)
STOPPED = Coords(x=0, y=0)


class Munchy(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = MunchyGame()

    @staticmethod
    def _get_rect(obj):
        return (obj.x * CELL_SIZE, obj.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def draw(self):
        self.screen.fill(BLACK)

        # draw apple
        apple_rect = self._get_rect(self.game.apple)
        pygame.draw.rect(self.screen, RED, pygame.Rect(*apple_rect))

        # draw snake
        for segment in self.game.snake:
            segment_rect = self._get_rect(segment)
            pygame.draw.rect(self.screen, BLUE, pygame.Rect(*segment_rect))

        # draw score
        score_surface = self.font.render(str(self.game.score), True, WHITE)
        self.screen.blit(score_surface, (0, 0))

        if not self.game.running:
            self.screen.blit(self.font.render("GAME OVER", True, WHITE), (0, 20))
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(SPEED)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self.game.update_snake_dir(event.key)
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.QUIT:
                    self.running = False
            self.game.update()
            self.draw()
        pygame.quit()


class MunchyGame(object):

    SNAKE_START_LENGTH = 8
    SNAKE_GROWTH = 4

    def __init__(self):
        self.snake_length = self.SNAKE_START_LENGTH
        self.snake_dir = STOPPED
        self.snake = collections.deque([Coords(CELL_WIDTH//2, CELL_HEIGHT//2)])
        self.apple = self._random_coords()
        self.score = 0
        self.running = True  # differs from Munchy's

    @staticmethod
    def _random_coords():
        x = random.randint(0, CELL_WIDTH-1)
        y = random.randint(0, CELL_HEIGHT-1)
        return Coords(x, y)

    def _move_apple(self):
        self.score += 1
        self.apple = self._random_coords()
        if self.apple in self.snake:
            self._move_apple()

    def _move_snake(self):
        if self.snake_dir == STOPPED:
            return
        head = self.snake[-1]
        new_x = head[0] + self.snake_dir.x
        new_y = head[1] + self.snake_dir.y
        self.snake.append(Coords(new_x, new_y))
        if len(self.snake) > self.snake_length:
            self.snake.popleft()

    def update_snake_dir(self, dir_key):
        dir_key_map = {pygame.K_UP: UP, pygame.K_DOWN: DOWN, pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}
        direction = dir_key_map[dir_key]
        opposite_dirs = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if self.snake_dir != opposite_dirs[direction]:
            self.snake_dir = direction

    def update(self):
        if self.running:
            self._move_snake()
        head = self.snake[-1]
        if head == self.apple:
            self._move_apple()
            self.snake_length += self.SNAKE_GROWTH

        # check for collisinon with snake body; deques do not support slice indexing
        for segment_index in range(len(self.snake) - 1):
            if head == self.snake[segment_index]:
                self.running = False

if __name__ == '__main__':
    Munchy().run()
