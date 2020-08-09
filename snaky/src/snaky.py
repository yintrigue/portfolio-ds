import pygame
import random
from collections import defaultdict
from sprites import SnakeSprite 

class Snaky:
    """A simple classic game, Snake, build using pygame. It is designed 
    specifically for nerual network training.
    """
    def __init__(self,
                 snake_sprite_sheet_url: str, 
                 apple_sprite_url: str,
                 font_url: str):
        # config constants
        self.__BOARD_COLOR = (255, 255, 255)
        self.__FRAMERATE = 60
        # block count; e.g. 20 means snake can only move 20 steps from top to 
        # bottom (or from left to right)
        self.__BOARD_DIM = 10 
        self.__BLOCK_DIM = 50 # pixel per block
        
        # game assets and clock
        self.__board = None # pygame.Surface
        self.__font_url = font_url
        self.__font = None # pygame.font
        self.__sprite = SnakeSprite(snake_sprite_sheet_url, 
                                    apple_sprite_url, 
                                    self.__BLOCK_DIM)
        self.__clock = pygame.time.Clock() 
        
        # positions of the snake's head, body parts, and tail
        bc = self.__BOARD_DIM // 2 # board center
        self.__snake = [(bc, bc), (bc, bc+1), (bc, bc+2)] 
        self.__apple = None # tuple, position of the apple
        
        # game states
        self.__score = 0
        self.__snake_direction = -1 # int
        
    def play(self, snake: list = []) -> None:
        """Start the pygame loop and render the default snake.
        """
        pygame.init()
        pygame.display.set_caption("SNAKY")
        if len(snake) >= 3:
            self.__snake = snake
        
        # build the game __board
        dim_pixel = self.__BLOCK_DIM * self.__BOARD_DIM
        self.__board = pygame.display.set_mode((dim_pixel, dim_pixel))
        self.__board.fill(self.__BOARD_COLOR)
        
        # load sprite sheet
        self.__sprite.load()
        self.__font = pygame.font.Font(self.__font_url, 28)
        
        # render the initial state
        self.__board.fill(self.__BOARD_COLOR)
        self.__update_snake() # render the first snake
        self.__update_apple(True)
        pygame.display.update()
            
        # start the game loop
        running = True
        while running:
            running = self.__handle_pygame_events()
            self.__clock.tick(self.__FRAMERATE)
        pygame.quit()
            
    def key_press(self, input_:int) -> bool:
        """Simulate user key press events.
        """
        if input_ not in [0, 1, 2, 3]:
            return False
        
        if input_ == 0:
            new_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        elif input_ == 1:
            new_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        elif input_ == 2:
            new_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        else:
            new_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        
        pygame.event.post(new_event)
        self.__handle_pygame_events()
        
        return True
    
    def __handle_pygame_events(self) -> bool:
        """Function to handle all game events.
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            else:
                key = self.__onkeydown(e)
                if key in [0, 1, 2, 3]:
                    result = self.__move_snake(key)

                    # 0 - No collision.
                    # 1 - Apple
                    # 2 - Self
                    # 3 - Wall
                    # -1 - Move not allowed (e.g. auto-protect)
                    if result == 2 or result == 3: # moved, collided, dead
                        self.__board.fill(self.__BOARD_COLOR)
                        self.__show_ending('Game Over')
                        pygame.display.update()
                    elif result == -1: # move not allowed
                        # do nothing for now
                        pass
                    else: # moved, survived, might have an apple
                        self.__board.fill(self.__BOARD_COLOR)
                        self.__update_snake()
                        self.__update_apple(result == 1)
                        pygame.display.update()

                elif key == pygame.K_q:
                    return False
                else:
                    # do nothing for now
                    pass
        return True
            
    def __relative_pos(self, 
                       p1: tuple, 
                       p2: tuple, 
                       p2_sprites: tuple) -> tuple:
        """Determine the position of p2 relative to p1. A proper sprite is 
        returned.
        """
        is_top = p1[1] > p2[1] and p1[0] == p2[0]
        is_right = p1[1] == p2[1] and p1[0] < p2[0]
        is_bottom = p1[1] < p2[1] and p1[0] == p2[0]
        is_left = p1[1] == p2[1] and p1[0] > p2[0]
        
        if is_top:
            return p2_sprites[0]
        if is_right:
            return p2_sprites[1]
        if is_bottom:
            return p2_sprites[2]
        if is_left:
            return p2_sprites[3]
        
        # catch all
        return p2_sprites[0]
    
    def __relative_turn(self, 
                        p1: tuple, 
                        p2: tuple,
                        p3: tuple,
                        p2_sprites: tuple,
                        p2_turn_sprites: tuple) -> tuple:
        """Determine the position of p2 relative to p1 and p3. A proper sprite 
        is returned.
        """
        # not turning; stright line
        if p1[0] == p2[0] and p2[0] == p3[0]:
            # vertical line
            is_top = p1[1] > p2[1] and p1[0] == p2[0]
            is_bottom = p1[1] < p2[1] and p1[0] == p2[0]
            
            if is_bottom:
                return p2_sprites[2]
            if is_top:
                return p2_sprites[0]
        if p1[1] == p2[1] and p2[1] == p3[1]:
            # horizontal line
            is_right = p1[1] == p2[1] and p1[0] < p2[0]
            is_left = p1[1] == p2[1] and p1[0] > p2[0]
            
            if is_right:
                return p2_sprites[1]
            if is_left:
                return p2_sprites[3]
        
        # turning clockwise
        right_bottom = p1[0] > p2[0] and p3[1] > p2[1]
        bottom_left = p1[1] > p2[1] and p3[0] < p2[0]
        left_top = p1[0] < p2[0] and p3[1] < p2[1]
        top_right = p1[1] < p2[1] and p3[0] > p2[0]

        if right_bottom:
            return p2_turn_sprites[0]
        if bottom_left:
            return p2_turn_sprites[1]
        if left_top:
            return p2_turn_sprites[2]
        if top_right:
            return p2_turn_sprites[3]
        
        # turning counter-clockwise
        right_bottom = p1[0] < p2[0] and p3[1] > p2[1]
        bottom_left = p1[1] < p2[1] and p3[0] < p2[0]
        left_top = p1[0] > p2[0] and p3[1] < p2[1]
        top_right = p1[1] > p2[1] and p3[0] > p2[0]

        if right_bottom:
            return p2_turn_sprites[4]
        if bottom_left:
            return p2_turn_sprites[5]
        if left_top:
            return p2_turn_sprites[6]
        if top_right:
            return p2_turn_sprites[7]
        
        # catch all condition
        return p2_sprites[0]
    
    def __show_ending(self, message:str) -> None:
        """Add ending screen to the game board.
        """
        surf = self.__font.render(message, True, (150, 150, 150))
        rect = surf.get_rect()
        rect.center = ((self.__BOARD_DIM * self.__BLOCK_DIM // 2), 
                       (self.__BOARD_DIM * self.__BLOCK_DIM // 2))
        self.__board.blit(surf, rect)
    
    def __update_apple(self, new_apple: bool = False) -> None:
        """Add an apple to the game board.
        """
        if new_apple:
            # generate a list of empty blocks
            empty_blocks = [(i, j) 
                            for i in range(self.__BOARD_DIM)
                            for j in range(self.__BOARD_DIM) 
                            if (i, j) not in self.__snake]

            if len(empty_blocks) == 0:
                # no more empty block, mission complete!
                return
        
            i = random.randrange(0, len(empty_blocks))
            self.__apple = empty_blocks[i]
        
        self.__board.blit(self.__sprite.apple, (self.__apple[0]*self.__BLOCK_DIM, 
                                                self.__apple[1]*self.__BLOCK_DIM))
    def __update_snake(self) -> None:
        """Update the snake on the game board according to the positions specified 
        by self.__snake.
        """
        for i, (x, y) in enumerate(self.__snake):
            if i == 0: # head
                head_pos = (x, y)
                body_pos= self.__snake[i+1]
                head = self.__relative_pos(body_pos, head_pos, self.__sprite.head)
                self.__board.blit(head, (x*self.__BLOCK_DIM, y*self.__BLOCK_DIM))
            elif i == len(self.__snake) - 1: # tail
                tail_pos = (x, y)
                body_pos= self.__snake[i-1]
                tail = self.__relative_pos(tail_pos, body_pos, self.__sprite.tail)
                self.__board.blit(tail, (x*self.__BLOCK_DIM, y*self.__BLOCK_DIM))
            else: # body
                head_pos = self.__snake[i-1] # part that proceeds body
                tail_pos = self.__snake[i+1] # part that follows body
                body_pos = (x, y)
                body = self.__relative_turn(head_pos, 
                                            body_pos, 
                                            tail_pos, 
                                            self.__sprite.body,
                                            self.__sprite.body_turn)
                # render sprite
                self.__board.blit(body, (x*self.__BLOCK_DIM, y*self.__BLOCK_DIM))
    
    def __collision_test(self, pos: tuple) -> int:
        """Detect if the snake collides with an object.
        Returns:
            (int):  0 - No collision.
                    1 - Apple
                    2 - Self
                    3 - Wall
        """
        if pos == self.__apple:
            # hit apple
            return 1
        elif pos in self.__snake:
            # hit self
            return 2
        elif (pos[0] < 0 or 
              pos[1] < 0 or 
              pos[0] >= self.__BOARD_DIM or 
              pos[1] >= self.__BOARD_DIM):
            # hit wall
            return 3
        else:
            return 0
        
    def __move_snake(self, d: int) -> int:
        """Move snake according to the direction given.
        Returns:
            (int):  0 - No collision.
                    1 - Apple
                    2 - Self
                    3 - Wall
                    -1 - Move not allowed (e.g. auto-protect)
        """
        # snake should not move backwards
        if ((d == 0 and self.__snake_direction == 2) or
            (d == 1 and self.__snake_direction == 3) or
            (d == 2 and self.__snake_direction == 0) or 
            (d == 3 and self.__snake_direction == 1)):
            # do nothing
            return -1
        
        # get snake's next position
        x, y = self.__snake[0]
        if d == 0:
            y -= 1
        elif d == 1:
            x += 1
        elif d == 2:
            y += 1
        elif d == 3:
            x -= 1
        
        # hit dectation
        hit = self.__collision_test((x, y))
        if hit == 0 or hit == 1: # apple or no collision
            
            # update direction
            self.__snake_direction = d 
            # add new head
            self.__snake = [(x, y)] + self.__snake
            # remove old tail only if no apple
            if hit == 0: 
                self.__snake.pop() 
            
            return hit
        else: # gameover
            return hit
    
    def __onkeydown(self, event: pygame.event) -> int:
        """Translate a key press event to a signal understood by the snake. In
        particular, arrow key events will be translated to the following int
        numbers:
              0
            3   1
              2
        Returns:
            (int): One of the pygame.key values. Possible values:
                pygame.K_q
                0 if pygame.K_UP
                1 if pygame.K_RIGHT
                2 if pygame.K_DOWN3
                3 if pygame.K_LEFT
                -1 for all other events inlcuding no key press.
        """
        if event.type != pygame.KEYDOWN:
            return -1
        
        if event.key == pygame.K_q:
            return event.key

        switch = {
            pygame.K_UP: 0,
            pygame.K_RIGHT: 1,
            pygame.K_DOWN: 2,
            pygame.K_LEFT: 3,
        }
        switch = defaultdict(lambda:-1, switch)
        key = switch[event.key]
        
        return key