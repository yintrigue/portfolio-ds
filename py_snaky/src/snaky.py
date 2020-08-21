import pygame
import random
import pandas as pd
from collections import defaultdict
from sprites import SnakeSprite
from itertools import count

class Snaky:
    """A simple classic game, Snake, build using pygame. It is designed
    specifically for nerual network training.
    """

    def __init__(self,
                 snake_sprite_sheet_url: str,
                 apple_sprite_url: str,
                 font_url: str) -> None:
        # config constants
        self.__BOARD_COLOR = (255, 255, 255)

        # block count; e.g. 20 means snake can only move 20 steps from top to
        # bottom (or from left to right)
        self.__BOARD_DIM = 10
        self.__BLOCK_DIM = 50 # pixel per block
        self.__FRAME_RATE = 60

        # game assets and clock
        self.__board = None # pygame.Surface
        self.__font_url = font_url
        self.__font = None # pygame.font
        self.__sprite = SnakeSprite(snake_sprite_sheet_url,
                                    apple_sprite_url,
                                    self.__BLOCK_DIM)
        self.__demo_fps = 10
        self.__clock = pygame.time.Clock()

        # initialize snake position and legnth
        self.__snake = []
        self.__apple = None # tuple, position of the apple
        self.reset()

        # moves that will be automatically played at the beginning of the game
        self.__moves = []

        # game states
        self.__score = 0
        self.__snake_direction = 0 # int; default to head up (i.e. 0)

    @property
    def vision(self) -> list:
        """Return what the snake can see around its head.
        Returns:
            (list) [up, right, down, left]; a list with each item indicating
                    the specific object type in one of the four possible directions.
                    0 - No collision
                    1 - Apple
                    2 - Self
                    3 - Wall
        """
        head_x, head_y = self.snake[0]
        u = head_x, head_y - 1
        r = head_x + 1, head_y
        d = head_x, head_y + 1
        l = head_x - 1, head_y

        return [self.__collision_test(u),
                self.__collision_test(r),
                self.__collision_test(d),
                self.__collision_test(l)]

    @property
    def head_direction(self) -> int:
        """
              0
            3   1
              2
        """
        return self.__snake_direction

    @property
    def head_pos(self) -> tuple:
        return self.__snake[0]

    @property
    def snake_len(self) -> int:
        return len(self.__snake)

    @property
    def snake(self) -> list:
        return self.__snake

    @snake.setter
    def snake(self, snake: list) -> None:
        if len(snake) >= 3:
            self.__snake = snake

            # update snake's head direction
            is_heading_up = self.__snake[0][1] - self.__snake[1][1]
            is_heading_right = self.__snake[0][0] - self.__snake[1][0]
            if is_heading_up != 0:
                if is_heading_up < 0:
                    self.__snake_direction = 0
                else:
                    self.__snake_direction = 2
            else:
                if is_heading_right > 0:
                    self.__snake_direction = 1
                else:
                    self.__snake_direction = 3

    def set_demo_fps(self, frame_rate:int) -> None:
        self.__demo_fps = frame_rate

    def set_moves(self, moves: list = []) -> None:
        self.__moves = moves

    def play(self, snake: list = []) -> None:
        """Start the pygame loop and render the default snake.
        """
        self.snake = snake

        pygame.init()
        pygame.display.set_caption("SNAKY")

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
        self.__update_display()

        # start the game loop
        running = True
        while running:
            # start listening to user events only if the "pre-moves" have been played
            if len(self.__moves) == 0:
                # start listening to pygame events
                running = self.__pygame_events_handler()
                # revert to the default frame rate once the "real" game startes
                self.__clock.tick(self.__FRAME_RATE)
            else:
                # "pre-moves"
                self.key_press(self.__moves.pop())
                self.__clock.tick(self.__demo_fps)
        self.quit()

    def reset(self) -> None:
        """Reset all game status including score, snake position, and snake length.
        """
        bc = self.__BOARD_DIM // 2 # default to board center
        self.__snake = [(bc, bc), (bc, bc+1), (bc, bc+2)]
        self.__update_apple(True)
        self.__snake_direction = 0

        self.__update_display()

    def quit(self):
        """Force quitting the game.
        """
        pygame.quit()

    def key_press(self, input_:int) -> bool:
        """Simulate user key press events.
        Direction encode:
            0
          3   1
            2
        """
        if input_ not in [0, 1, 2, 3]:
            return False

        if input_ == 0:
            new_event = pygame.event.Event(pygame.USEREVENT, key=pygame.K_UP)
        elif input_ == 1:
            new_event = pygame.event.Event(pygame.USEREVENT, key=pygame.K_RIGHT)
        elif input_ == 2:
            new_event = pygame.event.Event(pygame.USEREVENT, key=pygame.K_DOWN)
        else:
            new_event = pygame.event.Event(pygame.USEREVENT, key=pygame.K_LEFT)

        pygame.event.post(new_event)
        self.__pygame_events_handler()

        return True

    def __pygame_events_handler(self) -> bool:
        """Function to handle all game events.
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            else:
                key = self.__onkeydown(e)
                if key in [0, 1, 2, 3]:
                    result = self._move_snake(key)

                    # 0 - No collision.
                    # 1 - Apple
                    # 2 - Self
                    # 3 - Wall
                    if result == 2 or result == 3: # moved, collided, dead
                        self.__board.fill(self.__BOARD_COLOR)
                        self.__show_ending('Game Over')
                        self.__update_display()
                    else: # moved, survived, might have an apple
                        self.__board.fill(self.__BOARD_COLOR)
                        self.__update_snake()
                        self.__update_apple(result == 1)
                        self.__update_display()

                elif key == pygame.K_q:
                    return False
                else:
                    # do nothing for now
                    pass
        return True

    def __update_display(self) -> None:
        if pygame.get_init():
            pygame.display.update()

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
        rect.center = ((self.__BOARD_DIM * self.__BLOCK_DIM // 2) - 1,
                       (self.__BOARD_DIM * self.__BLOCK_DIM // 2) - 1)
        self.__board.blit(surf, rect)

    def __update_apple(self, new_apple=False) -> None:
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

        if pygame.get_init():
            self.__board.blit(self.__sprite.apple, (self.__apple[0]*self.__BLOCK_DIM,
                                                    self.__apple[1]*self.__BLOCK_DIM))
    def __update_snake(self) -> None:
        """Update the rendering of snake on the game board according to the positions
        of head, bodies, and tail specified by self.__snake.
        """
        for i, (x, y) in enumerate(self.__snake):
            if i == 0: # head
                head_pos = (x, y)
                body_pos= self.__snake[i+1]
                head = self.__relative_pos(body_pos, head_pos, self.__sprite.head)
                if pygame.get_init():
                    self.__board.blit(head, (x*self.__BLOCK_DIM, y*self.__BLOCK_DIM))

            elif i == len(self.__snake) - 1: # tail
                tail_pos = (x, y)
                body_pos= self.__snake[i-1]
                tail = self.__relative_pos(tail_pos, body_pos, self.__sprite.tail)
                if pygame.get_init():
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
                if pygame.get_init():
                    self.__board.blit(body, (x*self.__BLOCK_DIM, y*self.__BLOCK_DIM))

    def __collision_test(self, pos: tuple) -> int:
        """Detect if the snake collides with an object.
        Returns:
            (int):  0 - No collision
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

    def _move_snake(self, d: int) -> int:
        """Move snake according to the direction given.
        Returns:
            (int):  0 - No collision
                    1 - Apple
                    2 - Self
                    3 - Wall
        """
        # snake should not move backwards; if a backwards direction is entered,
        # the snake will take one step towards where the snake is currently heading
        d = self.__snake_direction if abs(d - self.__snake_direction) == 2 else d

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

        # collision dectation
        hit = self.__collision_test((x, y))
        if hit == 0 or hit == 1: # apple or no collision
            self.__snake_direction = d # update direction
            self.__snake = [(x, y)] + self.__snake # add new head

            # remove old tail only if no apple
            if hit == 0:
                self.__snake.pop()

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
        # validating inputs
        if event.type != pygame.KEYDOWN and event.type != pygame.USEREVENT:
            return -1
        if event.key == pygame.K_q:
            return event.key
        if event.key not in [pygame.K_UP,
                             pygame.K_RIGHT,
                             pygame.K_DOWN,
                             pygame.K_LEFT]:
            return -1

        switch = {
            pygame.K_UP: 0,
            pygame.K_RIGHT: 1,
            pygame.K_DOWN: 2,
            pygame.K_LEFT: 3,
        }
        switch = defaultdict(lambda:-1, switch)
        key = switch[event.key]

        return key

class SnakySimulator(Snaky):
    """Same as Snake but no game loop will be started, no user events will
    be received, and no visuals will be rendered.
    """

    def __init__(self,
                 snake_sprite_sheet_url: str,
                 apple_sprite_url: str,
                 font_url: str) -> None:
        super().__init__(snake_sprite_sheet_url,
                         apple_sprite_url,
                         font_url)

    def replay(self, game_id: int = 0, csv:str = 'snaky.csv', fps:int = 2) -> None:
        """Reply the game store in csv.
        """
        df = pd.read_csv(csv)
        df = df.loc[df.game_id == game_id, :]
        moves = df['move'].to_list()

        super().set_demo_fps(fps)
        super().set_moves(moves)
        super().play()

    def simulate(self,
                 num_game: int = 100,
                 snake: list = [],
                 csv: str = 'snaky.csv') -> None:
        """ Auto play data and save game data to CSV.
        Direction encode:
            0
          3   1
            2
        Hit encode:
            0 - No collision
            1 - Apple
            2 - Self
            3 - Wall
        """
        if len(snake) >= 3:
            super().__snake = snake

        examples = {
            'game_id': [],
            'move_id': [],

            'vision': [], # int, 4 digits, each indicates the object that the snake "sees"
            'snake_length': [], # int, direction encode
            'head_direction': [], # int
            'head_pos': [], # tuple

            'move': [], # int, direction encode
            'vision_new': [], # int, direction encode
            'snake_length_new': [], # int
            'head_direction_new': [], # int, direction encode
            'head_pos_new': [], # tuple

            'hit': [], # hit encode
            'life': [] # 0: dead, 1: dead
        }

        for i in range(num_game):
            j = 0
            for j in count(0):
                examples['game_id'].append(i)
                examples['move_id'].append(j)

                examples['vision'].append(''.join([str(d) for d in super().vision]))
                examples['snake_length'].append(super().snake_len)
                examples['head_direction'].append(super().head_direction)
                examples['head_pos'].append((super().head_pos[0], super().head_pos[1]))

                # move snake & get result
                move = random.randrange(0, 4)
                hit = super()._move_snake(move)
                if hit == 2 or hit == 3:
                    life = 0
                else:
                    life = 1

                examples['move'].append(move)
                examples['vision_new'].append(''.join([str(d) for d in super().vision]))
                examples['snake_length_new'].append(super().snake_len)
                examples['head_direction_new'].append(super().head_direction)
                examples['head_pos_new'].append((super().head_pos[0], super().head_pos[1]))

                examples['hit'].append(hit)
                examples['life'].append(life)

                if life == 0:
                    super().reset()
                    break

        df = pd.DataFrame(examples)
        df.to_csv(csv, index=False)
        print('A total of {:,d} examples have been generated...'.format(df.shape[0]))
