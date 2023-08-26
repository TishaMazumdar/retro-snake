import pygame, sys, random
from pygame.math import Vector2
pygame.init()

cell_size = 30
cell_no = 20
pygame.display.set_caption('retro-snake')
screen = pygame.display.set_mode((cell_no*cell_size, cell_no*cell_size))
game_font = pygame.font.SysFont('Terminal',40)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
    
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, self.random_color(), snake_rect)
    
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def random_color(self):
        while True:
            red = random.randint(128,255)
            green = random.randint(128,255)
            blue = random.randint(128,255)

            if green + blue > 150 or red < 200:
                return red,green,blue
    
class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size) ,cell_size, cell_size)
        pygame.draw.rect(screen, 'red', fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_no - 1)
        self.y = random.randint(0, cell_no - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self,screen_update_event):
        self.snake = SNAKE()
        self.fruit = FRUIT()

        self.SCREEN_UPDATE = screen_update_event

        # support lines
        self.support_line_surf = pygame.Surface((cell_no * cell_size, cell_no * cell_size))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(20)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grid()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            pygame.time.set_timer(self.SCREEN_UPDATE, self.calculate_interval())

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_no or not 0 <= self.snake.body[0].y < cell_no:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        lost_text = game_font.render("GAME OVER", 1, 'white')
        screen.blit(lost_text, ((cell_no * cell_size)/2 - lost_text.get_width()/2, (cell_no * cell_size)/2 - lost_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(4000)
        pygame.quit()
        sys.exit()
    
    def draw_grid(self):
        self.support_line_surf.fill('green')
        for x in range(0, cell_no * cell_size, cell_size):
            pygame.draw.line(self.support_line_surf, (255, 255, 255), (x, 0), (x, cell_no * cell_size))
        for y in range(0, cell_no * cell_size, cell_size):
            pygame.draw.line(self.support_line_surf, (255, 255, 255), (0, y), (cell_no * cell_size, y))
        
        screen.blit(self.support_line_surf,(0,0))
    
    def draw_score(self):
        score_text = "Score: " + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, 'white')

        score_x = int(cell_size * cell_no - 65)
        score_y = int(cell_size * cell_no - 20)
        score_rect = score_surface.get_rect(center = (score_x, score_y))

        screen.blit(score_surface, score_rect)
    
    def calculate_interval(self):
        speed_increase_intervals = 5  # Adjust speed every 5 points
        speed_increase_value = 3 * speed_increase_intervals  # The amount of decrease in milliseconds
        score = len(self.snake.body) - 3
        return max(50, 150 - (score // speed_increase_intervals) * speed_increase_value)

def main():
    clock = pygame.time.Clock()
    framerate = 60

    SCREEN_UPDATE = pygame.USEREVENT
    main_game = MAIN(SCREEN_UPDATE)
    pygame.time.set_timer(SCREEN_UPDATE, main_game.calculate_interval())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == SCREEN_UPDATE:
                main_game.update()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
        
        screen.fill('black')
        main_game.draw_elements()
        pygame.display.update()     # draw all our elements
        clock.tick(framerate)

if __name__ == '__main__':
    main()
