import pygame
import random
import numpy as np
import pandas as pd

from typing import Union
from collections import defaultdict
from sprites import SnakeSprite
from itertools import count

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, InputLayer, BatchNormalization
from tensorflow.keras.optimizers import Adam

from sklearn.metrics import classification_report

class Snaky:
    """A simple classic game, Snake, build using pygame. It is designed for
    nerual net training.
    """
    # collision detection codes
    COLLIDE_NONE = 0
    COLLIDE_APPLE = 1
    COLLIDE_HEAD = 2
    COLLIDE_NECK = 3
    COLLIDE_BODY = 4
    COLLIDE_WALL = 5

    # pygame configs
    BOARD_DIM = 10 # dimension of game board (pygame surface) as # of blocks
    BLOCK_EDGE_RESOLUTION = 50 # pixel per block edge
    FRAME_RATE = 60

    def __init__(self,
                 snake_sprite_sheet_url: str,
                 apple_sprite_url: str,
                 font_url: str,
                 board_color: list = (255, 255, 255)) -> None:
        # pygame assets and clock
        self.__board = None # pygame.Surface
        self.__board_color = board_color
        self.__font_url = font_url
        self.__enable_ending = True # set true to show ending at game over
        self.__sprite = SnakeSprite(snake_sprite_sheet_url,
                                    apple_sprite_url,
                                    Snaky.BLOCK_EDGE_RESOLUTION)
        self.__clock = pygame.time.Clock()

        # initialize snake position and legnth
        self.__snake = []
        self.__apple = None # tuple, position of the apple
        self.reset()

        # replay properties
        self.__replay_moves = []
        self.__replay_apples = []
        self.__replay_fps = 10

        # game states
        self.__score = 0
        self.__snake_direction = 0 # int; default to head up (i.e. 0)
        self.__game_state = 1 # 0: quit, 1: play, 2: game_over

        # game scores
        self.__n_apple = 0
        self.__n_step = 0

    @property
    def vision(self) -> list:
        """Snake sees the objects around its head.
        Returns:
            (list) [up, right, down, left]; a list with each item indicating
                    the specific object type in one of the four possible directions.
                    (int):  Snaky.COLLIDE_NONE
                            Snaky.COLLIDE_APPLE
                            Snaky.COLLIDE_BODY
                            Snaky.COLLIDE_NECK
                            Snaky.COLLIDE_WALL
        """
        return self.__get_vision(self.snake[0])

    @property
    def vision_simple(self) -> list:
        """Snake sees a "simplified" world.
        Returns:
            (list) [up, right, down, left]; a list with each item indicating
                    the specific object type in one of the four possible directions.
            (int):  Snaky.COLLIDE_NONE -> 1
                    Snaky.COLLIDE_APPLE -> 1
                    Snaky.COLLIDE_BODY -> 0
                    Snaky.COLLIDE_NECK -> 0
                    Snaky.COLLIDE_WALL -> 0
        """
        return self.to_vision_simple(self.vision).tolist()

    @property
    def vision_advanced(self) -> list:
        """Snake sees the location of apple in addition to what's around it. That
        is: self.vision_simple + self.vision_apple
        Returns:
            (list): A list of 8.
                [v, v, v, v, a, a, a, a]
                [0]-[3]: self.vision_simple
                [4]-[7]: self.vision_apple
        """
        v_apple = self.vision_apple(self.head_pos, self.apple_pos)
        v = self.vision_simple
        v.extend(v_apple)
        return v

    @property
    def vision_expert(self) -> list:
        """Snake sees if a direction would lead to a dead end. A deadend is
        defined as an area that is fully enclosed by snake's body or wall.
        Returns:
            (list): A list of 12.
                [v, v, v, v, a, a, a, a, c, c, c, c]
                [0]-[3]: self.vision_simple
                [4]-[7]: self.vision_apple
                [8]-[11]: 0 if a closed region is formed; 1 otherwise
        """
        head_x, head_y = self.snake[0]
        u = head_x, head_y - 1
        r = head_x + 1, head_y
        d = head_x, head_y + 1
        l = head_x - 1, head_y
        v_closed_region = [
                        self.test_closed_region(u, self.snake),
                        self.test_closed_region(r, self.snake),
                        self.test_closed_region(d, self.snake),
                        self.test_closed_region(l, self.snake)]
        v = self.vision_advanced
        v.extend(v_closed_region)
        return v

    def vision_apple(self, head_pos: tuple, apple_pos: tuple) -> tuple:
        """Snake sees if a direction would lead to an apple.
        Returns:
            [0] Apple above.
            [1] Apple on the right.
            [2] Apple below.
            [3] Apple on the left.
        """
        head_x, head_y = head_pos
        apple_x, apple_y = apple_pos

        u = 1 if (apple_y - head_y) < 0 else 0
        r = 1 if (apple_x - head_x) > 0 else 0
        d = 1 if (apple_y - head_y) > 0 else 0
        l = 1 if (apple_x - head_x) < 0 else 0

        return u, r, d, l

    def test_closed_region(
                        self,
                        pos:tuple,
                        snake: list,
                        is_pos_head: bool = False) -> int:
        """Snake sees if taking the next move would form a closed region on map.
        """
        visions = self.__get_vision(pos)
        visions_arr = np.array(visions)

        # scenario 0: pos is a part of the snake's body; dead = closed region
        if is_pos_head:
            # exclude head and tail
            snake_parts = snake[1: len(snake)-1]
        else:
            # exclude tail
            snake_parts = snake[: len(snake)-1]
        if pos in snake_parts:
            return 1

        # scenario 1: no closed region anywhere; this should be the majority
        if (Snaky.COLLIDE_BODY not in visions) and (Snaky.COLLIDE_WALL not in visions):
            # not possible to form a closed region if the head is not in contact
            # with a body part or wall
            return 0

        # scenario 2: snake forms a closed region without the help of wall
        if visions.count(Snaky.COLLIDE_NONE) == 2 and Snaky.COLLIDE_WALL not in visions:
            collision_i_arr = np.where(visions_arr == Snaky.COLLIDE_NONE)[0]
            if abs(collision_i_arr[0] - collision_i_arr[1]) == 2:
                # snake's head is connected to its body AND the two spaces are
                # on the two sides (up & down, or left & right)
                return 1

        # scenario 3: snake forms a closed region with the help of wall
        if Snaky.COLLIDE_WALL in visions:
            i_wall = None
            i_no_wall = None
            snake_body = snake[1: len(snake)-1]

            for i, body_pos in enumerate(snake_body):
                body_vision = self.__get_vision(body_pos)

                # find first body part NOT in contact with wall
                if i_no_wall is None and Snaky.COLLIDE_WALL not in body_vision:
                    i_no_wall = i

                # find first body part in contact with wall
                if i_wall is None and Snaky.COLLIDE_WALL in body_vision:
                    i_wall = i
                    if i_wall <= 1:
                        # first or second body part in contact with wall; there
                        # is no room for making a closed region
                        return 0

                # both cases are found
                if i_wall is not None and i_no_wall is not None:
                    if i_no_wall < i_wall:
                        # at least one body part is NOT in contact with the wall;
                        # THEN, at least one body part is in contact with the wall
                        return 1

        return 0

    def __get_vision(self, head_pos: tuple = ()) -> list:
        """Snake sees the objects around its head.
        Returns:
            (list) [up, right, down, left]; a list with each item indicating
                    the specific object type in one of the four possible directions.
                    (int):  Snaky.COLLIDE_NONE
                            Snaky.COLLIDE_APPLE
                            Snaky.COLLIDE_BODY
                            Snaky.COLLIDE_NECK
                            Snaky.COLLIDE_WALL
        """
        if len(head_pos) == 0:
            return None

        head_x, head_y = head_pos
        u = head_x, head_y - 1
        r = head_x + 1, head_y
        d = head_x, head_y + 1
        l = head_x - 1, head_y

        return [self.__collision_test(u),
                self.__collision_test(r),
                self.__collision_test(d),
                self.__collision_test(l)]

    def to_vision_simple(self, vision: Union[str, list]) -> np.ndarray:
        """Convert "regular" vision (defined by self.vision) to "simplified" vision.
        Returns:
            (list): self.vision_simple.
        """
        survival_code = [Snaky.COLLIDE_NONE, Snaky.COLLIDE_APPLE]
        if type(vision) == str:
            return np.array([1 if int(v) in survival_code else 0 for v in list(vision)])
        else:
            return np.array([1 if v in survival_code else 0 for v in vision])

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
    def apple_pos(self) -> tuple:
        return self.__apple

    @property
    def snake_len(self) -> int:
        return len(self.__snake)

    @property
    def snake(self) -> list:
        return self.__snake

    @snake.setter
    def snake(self, snake_list: list) -> None:
        if len(snake_list) < 3:
            return

        self.__snake = snake_list

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

    def enable_ending(self, ending: bool) -> None:
        self.__enable_ending = ending

    def replay(self,
               game_id: int = 0,
               fps:int = 2,
               ending: bool = False,
               csv:str = 'Snaky.csv',
               print_data: bool = False,
               delay: int = 1000) -> None:
        """Reply the game store in csv.
        """
        df = pd.read_csv(csv, dtype={'vision': np.object,
                                     'vision_simple': np.object,
                                     'vision_advanced': np.object,
                                     'vision_expert': np.object,
                                     'vision_new': np.object})
        df = df.loc[df.game_id == game_id, :]
        if print_data:
            print(df)

        self.__replay_moves = df['move'].to_list()
        self.__replay_apples = df['apple_pos_new'].to_list()
        self.__replay_fps = fps
        self.enable_ending(ending)

        self.play(delay=delay)

    def play(self, snake: list = [], delay: int = 0) -> None:
        """Start the pygame loop and render the default snake.
        """
        self.snake = snake
        pygame.init()
        pygame.display.set_caption("Snaky")

        # build the game __board
        dim_pixel = Snaky.BLOCK_EDGE_RESOLUTION * Snaky.BOARD_DIM
        self.__board = pygame.display.set_mode((dim_pixel, dim_pixel))
        self.__board.fill(self.__board_color)

        # load sprite sheet
        self.__sprite.load()

        # render the initial state
        self.__update_snake() # render the first snake
        if len(self.__replay_apples) > 0:
            self._update_apple(True, eval(self.__replay_apples[0]))
        else:
            self._update_apple(True)
        self.__update_display()

        # delay the reply at the beginning; this gives some time for the pygame
        # window to get ready
        pygame.time.delay(delay)

        # start the game loop
        running = True
        i = 0
        while self.__game_state != 0:
            # start listening to user events only if the "pre-moves" have been played
            if len(self.__replay_moves) == 0:
                # start listening to pygame events
                self.__game_state = self.__pygame_events_handler()
                i += 1
                # revert to the default frame rate once the replay ends
                self.__clock.tick(Snaky.FRAME_RATE)
            else:
                # replay
                self.key_press(self.__replay_moves.pop(0), self.__replay_apples.pop(0))
                self.__clock.tick(self.__replay_fps)

        print('Game over! Have a nice day!')
        self.quit()

    def reset(self) -> None:
        """Reset all game status including score, snake position, and snake length.
        """
        bc = Snaky.BOARD_DIM // 2 # default to board center
        self.__snake = [(bc, bc), (bc, bc+1), (bc, bc+2)]
        self._update_apple(True)
        self.__snake_direction = 0
        self.__n_apple = 0
        self.__nsteps = 0

        self.__update_display()

    def quit(self):
        """Force quitting the game.
        """
        pygame.quit()

    def key_press(self, move: int, apple_pos: tuple = None) -> bool:
        """Simulate user key press events.
        Direction encode:
            0
          3   1
            2
        """
        if move not in [0, 1, 2, 3]:
            return False

        if move == 0:
            new_event = pygame.event.Event(
                            pygame.USEREVENT, key=pygame.K_UP, apple=apple_pos)
        elif move == 1:
            new_event = pygame.event.Event(
                            pygame.USEREVENT, key=pygame.K_RIGHT, apple=apple_pos)
        elif move == 2:
            new_event = pygame.event.Event(
                            pygame.USEREVENT, key=pygame.K_DOWN, apple=apple_pos)
        else:
            new_event = pygame.event.Event(
                            pygame.USEREVENT, key=pygame.K_LEFT, apple=apple_pos)

        pygame.event.post(new_event)
        self.__pygame_events_handler()

        return True

    def __pygame_events_handler(self) -> int:
        """Function to handle all game events.
        Returns:
            (int): Game state. 0-quit, 1-play, 2-game_over
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0
            elif self.__game_state == 2:
                # skip all events below if the game is over
                continue
            else:
                # pull key press event
                key = self.__onkeydown(e)

                # handle quit event
                if key == pygame.K_q:
                    return 0

                # pull apple position
                if e.type == pygame.USEREVENT:
                    # pull apple position; pygame.USEREVENT happens only when
                    # the event is programatically generated through codes
                    apple_pos = eval(e.apple)
                else:
                    # pygame.KEYDOWN; happens when user actually presses a key
                    apple_pos = None

                # handle key events that indicate move directions
                if key in [0, 1, 2, 3]:
                    hit = self._move_snake(key)
                    if hit in [Snaky.COLLIDE_BODY,
                               Snaky.COLLIDE_NECK,
                               Snaky.COLLIDE_WALL]:
                        if self.__enable_ending:
                            self.__board.fill(self.__board_color)
                            self.__show_ending()
                            self.__update_display()
                            # game over
                            return 2
                    else:
                        self.__n_step += 1
                        self.__board.fill(self.__board_color)
                        self.__update_snake()

                        if apple_pos is not None:
                            # apple position is supplied, use it
                            self._update_apple(True, apple_pos)
                        else:
                            # update apple only if the snake just ate one
                            if hit == Snaky.COLLIDE_APPLE:
                                self.__n_apple += 1
                            self._update_apple(hit == Snaky.COLLIDE_APPLE)

                        self.__update_display()

                        # testing for self.test_closed_region
                        d = self.__snake_direction
                        x, y = self.__snake[0]
                        if d == 0:
                            y -= 1
                        elif d == 1:
                            x += 1
                        elif d == 2:
                            y += 1
                        elif d == 3:
                            x -= 1
                        v = self.test_closed_region((x, y), self.__snake)

        # no event received; keep the current game state
        return self.__game_state

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

    def __show_ending(self) -> None:
        """Add ending screen to the game board.
        """
        game_over_ft = pygame.font.Font(self.__font_url, 28)
        surf_go = game_over_ft.render('Game Over', True, (100, 100, 100))
        rect_go = surf_go.get_rect()
        rect_go.center = ((Snaky.BOARD_DIM * Snaky.BLOCK_EDGE_RESOLUTION // 2),
                          ((Snaky.BOARD_DIM - 1) * Snaky.BLOCK_EDGE_RESOLUTION // 2))
        self.__board.blit(surf_go, rect_go)

        text_step = 'STEPS' if self.__n_step > 1 else 'STEP'
        text_apple = 'APPLES' if self.__n_apple > 1 else 'APPLE'
        score = '{:,d} {} - {:,d} {}'.format(
                                        self.__n_step,
                                        text_step,
                                        self.__n_apple,
                                        text_apple)
        score_ft = pygame.font.Font(self.__font_url, 14)
        surf_sc = score_ft.render(score, True, (100, 100, 100))
        rect_sc = surf_sc.get_rect()
        rect_sc.center = ((Snaky.BOARD_DIM * Snaky.BLOCK_EDGE_RESOLUTION // 2),
                          (Snaky.BOARD_DIM * Snaky.BLOCK_EDGE_RESOLUTION // 2))
        self.__board.blit(surf_sc, rect_sc)

    def _update_apple(self, new_apple=False, pos: tuple = None) -> tuple:
        """Add an apple to the game board.
        """
        if new_apple:
            if pos is not None:
                self.__apple = pos
            else:
                # generate a list of empty blocks
                empty_blocks = [(i, j)
                                for i in range(Snaky.BOARD_DIM)
                                for j in range(Snaky.BOARD_DIM)
                                if (i, j) not in self.__snake]

                if len(empty_blocks) == 0:
                    # no more empty block, mission complete!
                    return None

                i = random.randrange(0, len(empty_blocks))
                self.__apple = empty_blocks[i]

        # add apple to blit if pygame is initiated
        if pygame.get_init():
            self.__board.blit(self.__sprite.apple, (self.__apple[0]*Snaky.BLOCK_EDGE_RESOLUTION,
                                                    self.__apple[1]*Snaky.BLOCK_EDGE_RESOLUTION))
        return self.__apple

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
                    self.__board.blit(head, (x*Snaky.BLOCK_EDGE_RESOLUTION, y*Snaky.BLOCK_EDGE_RESOLUTION))

            elif i == len(self.__snake) - 1: # tail
                tail_pos = (x, y)
                body_pos= self.__snake[i-1]
                tail = self.__relative_pos(tail_pos, body_pos, self.__sprite.tail)
                if pygame.get_init():
                    self.__board.blit(tail, (x*Snaky.BLOCK_EDGE_RESOLUTION, y*Snaky.BLOCK_EDGE_RESOLUTION))

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
                    self.__board.blit(body, (x*Snaky.BLOCK_EDGE_RESOLUTION, y*Snaky.BLOCK_EDGE_RESOLUTION))

    def __collision_test(self, pos: tuple, vision: bool = True) -> int:
        """Detect if the snake collides with an object. Note that the snake
        consists of three parts: Head, Neck (part immediately after head), Body,
        Tail (last part of the body).

        Args:
            pos (tuple): Position where the collision test will be performed.
            vision (bool): Set true to look ahead and "foresee" if the collision
                would occur. An edgy case is that it is safe to move onto its own
                tail (because the tail will be gone by the time the head move onto
                the block).

        Returns:
            (int):  Snaky.COLLIDE_NONE
                    Snaky.COLLIDE_APPLE
                    Snaky.COLLIDE_HEAD
                    Snaky.COLLIDE_BODY
                    Snaky.COLLIDE_NECK
                    Snaky.COLLIDE_WALL
        """
        if pos == self.__apple:
            # hit apple
            return Snaky.COLLIDE_APPLE
        elif pos in self.__snake:
            body_part_hit = self.__snake.index(pos)
            if body_part_hit == 0:
                # hit head; this is only possible if the vision is not performed
                # from the snake's head
                return Snaky.COLLIDE_HEAD
            elif body_part_hit == 1:
                # hit neck
                return Snaky.COLLIDE_NECK
            elif body_part_hit == len(self.__snake)-1:
                # hit tail
                if vision:
                    # snake is fine; tail will eb gone by the time the head
                    # moves onto the block
                    return Snaky.COLLIDE_NONE
                else:
                    return Snaky.COLLIDE_BODY
            else:
                # hit body
                return Snaky.COLLIDE_BODY
        elif (pos[0] < 0 or
              pos[1] < 0 or
              pos[0] >= Snaky.BOARD_DIM or
              pos[1] >= Snaky.BOARD_DIM):
            # hit wall
            return Snaky.COLLIDE_WALL
        else:
            return Snaky.COLLIDE_NONE

    def _move_snake(self, d: int) -> int:
        """Move snake according to the direction given.
        Args:
            d (int):
                      0
                    3   1
                      2
        Returns:
            (int):  Refer to the return of self.__collision_test().
        """
        # get snake's next position
        self.__snake_direction = d
        x, y = self.__snake[0]
        if d == 0:
            y -= 1
        elif d == 1:
            x += 1
        elif d == 2:
            y += 1
        elif d == 3:
            x -= 1

        # collision detection
        hit = self.__collision_test((x, y))
        if hit in [Snaky.COLLIDE_NONE, Snaky.COLLIDE_APPLE]:
            # update snake only if there is an apple or no collision
            self.__snake = [(x, y)] + self.__snake # add new head
            if hit != Snaky.COLLIDE_APPLE:
                # remove the tail if not an apple
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

class SmartSnaky(Snaky):
    """Same as Snake but no game loop will be started, no user events will
    be received, and no visuals will be rendered.
    """

    def __init__(self,
                 snake_sprite_sheet_url: str,
                 apple_sprite_url: str,
                 font_url: str,
                 board_color: list = (255, 255, 255)) -> None:
        super().__init__(snake_sprite_sheet_url,
                         apple_sprite_url,
                         font_url,
                         board_color)
        self.__brain_model = None # Sequential

    def simulate(
            self,
            n_game: int = 100,
            n_move: int = None,
            csv: str = 'snaky.csv',
            vision_mode: str = 'simple',
            use_brain: bool = False,
            brain_model: Sequential = None,
            verbose: bool = False) -> None:
        """Autoplay data and save game data to CSV.
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
        if brain_model is not None:
            self.brain_model = brain_model

        examples = {
            'game_id': [],
            'move_id': [],

            'vision': [], # int, 4 digits, each indicates the object that the snake "sees"
            'vision_simple': [],
            'vision_advanced': [],
            'vision_expert': [],
            'snake_length': [], # int, direction encode
            'head_direction': [], # int
            'head_pos': [], # tuple
            'apple_pos': [], # tuple

            'move': [], # int, direction encode
            'apple_pos_new': [], # tuple
            'facing_apple': [], # 1 if on the way to apple; 0 otherwise
            'closed_region': [], # 1 if closed region is formed; 0 otherwise
            'hit': [], # hit encode
            'life': [], # 0: dead, 1: dead
            'prob_to_live': [] # float
        }

        for i in range(n_game):
            if verbose:
                print(f'Playing game {i}...')
            j = 0
            for j in count(0):
                # --------------------------------------------------------------
                # SAVE PRE-MOVE DATA
                # get visions
                vision = ''.join([str(d) for d in super().vision])
                vision_simple = ''.join([str(d) for d in super().vision_simple])
                vision_advanced = ''.join([str(d) for d in super().vision_advanced])
                vision_expert = ''.join([str(d) for d in super().vision_expert])

                # save examples
                examples['game_id'].append(i)
                examples['move_id'].append(j)

                examples['vision'].append(vision)
                examples['vision_simple'].append(vision_simple)
                examples['vision_advanced'].append(vision_advanced)
                examples['vision_expert'].append(vision_expert)

                examples['snake_length'].append(super().snake_len)
                examples['head_direction'].append(super().head_direction)
                examples['head_pos'].append(super().head_pos)
                examples['apple_pos'].append(super().apple_pos)

                # --------------------------------------------------------------
                # GENERATE NEXT MOVE
                # generate the move; move is random if not using brain
                prob_to_live = None
                if use_brain and (self.__brain_model is not None):
                    move_options = tf.keras.utils.to_categorical(list(range(4)))
                    if vision_mode == 'simple':
                        # simple: sees obstacles
                        # labels:
                        # 0 - dead
                        # 1 - survived
                        vision = super().vision_simple

                        # predict the survival probability in each direction
                        life_probs = np.zeros(4)
                        for direction, move_option in enumerate(move_options):
                            # inputs: [v, v, v, v, m, m, m, m]
                            inputs = np.concatenate((vision, move_option)).reshape(1, 8)
                            prob = self.__brain_model.predict(inputs)
                            life_probs[direction] = prob

                        # select the move with the highest prob to survive
                        move = np.argmax(life_probs)
                        prob_to_live = life_probs[move]
                    elif vision_mode == 'advanced':
                        # advanced: sees obstacles + apple
                        # labels:
                        # 0 - dead
                        # 1 - survived && apple way
                        # 2 - survived && not apple way
                        vision = super().vision_advanced

                        # calculate the probability to survive in each direction
                        predicted_move_labels = [0] * 4
                        move_confidence = [0] * 4
                        for direction, move_option in enumerate(move_options):
                            # inputs: [v, v, v, v, v, v, v, v, m, m, m, m]
                            inputs = np.concatenate((vision, move_option)).reshape(1, 12)
                            probs = self.__brain_model.predict(inputs).flatten()
                            pred_label = np.argmax(probs)
                            predicted_move_labels[direction] = pred_label
                            move_confidence[direction] = probs[pred_label]

                        # select the move with the highest prob to survive
                        if predicted_move_labels.count(0) == 4:
                            # all move direction lead to death; just move up
                            move = 0
                            prob_to_live = 0
                        else:
                            if 1 in predicted_move_labels:
                                move = predicted_move_labels.index(1)
                            elif 2 in predicted_move_labels:
                                move = predicted_move_labels.index(2)
                            prob_to_live = move_confidence[move]
                    elif vision_mode == 'expert':
                        # expert: sees obstacles + apple + closed_region
                        # labels:
                        # 0 - dead
                        # 1 - survived && apple && !closed
                        # 2 - survived && !apple && !closed
                        # 3 - survived && apple && closed
                        # 4 - survived && !apple && closed
                        vision = super().vision_expert

                        # calculate the probability to survive in each direction
                        predicted_move_labels = [0] * 4
                        move_confidence = [0] * 4
                        for direction, move_option in enumerate(move_options):
                            # inputs: [v, v, v, v, v, v, v, v, v, v, v, v, m, m, m, m]
                            inputs = np.concatenate((vision, move_option)).reshape(1, 16)
                            probs = self.__brain_model.predict(inputs).flatten()
                            pred_label = np.argmax(probs)
                            predicted_move_labels[direction] = pred_label
                            move_confidence[direction] = probs[pred_label]

                        # predict and select best move
                        if predicted_move_labels.count(0) == 4:
                            # all move direction lead to death; just move up
                            move = 0
                            prob_to_live = 0
                        else:
                            if 1 in predicted_move_labels:
                                move = predicted_move_labels.index(1)
                            elif 2 in predicted_move_labels:
                                move = predicted_move_labels.index(2)
                            elif 3 in predicted_move_labels:
                                move = predicted_move_labels.index(3)
                            elif 4 in predicted_move_labels:
                                move = predicted_move_labels.index(4)
                            prob_to_live = move_confidence[move]
                    else:
                        print('Error: Invalid vision...')
                else:
                    # move snake randomly & get result
                    move = random.randrange(0, 4)

                # --------------------------------------------------------------
                # EXECUTE MOVE
                # execute the move
                facing_apple = self.__facing_apple(
                                            move,
                                            super().head_pos,
                                            super().apple_pos)
                hit = super()._move_snake(move)
                if hit in [Snaky.COLLIDE_BODY,
                           Snaky.COLLIDE_WALL,
                           Snaky.COLLIDE_NECK]:
                    life = 0
                else:
                    if hit == Snaky.COLLIDE_APPLE:
                        super()._update_apple(True)
                    life = 1

                # --------------------------------------------------------------
                # SAVE MOVE RESULTS
                # determine if a closed region is formed
                closed_region = super().test_closed_region(
                                                super().head_pos,
                                                super().snake,
                                                True)

                # save execution results
                examples['move'].append(move)
                examples['apple_pos_new'].append(super().apple_pos)
                examples['facing_apple'].append(facing_apple)
                examples['closed_region'].append(closed_region)
                examples['hit'].append(hit)
                examples['life'].append(life)
                examples['prob_to_live'].append(prob_to_live)

                if (life == 0) or ((n_move is not None) and (j > n_move)):
                    super().reset()
                    break

        df = pd.DataFrame(examples)
        df.to_csv(csv, index=False)
        print('A total of {:,d} examples have been generated...'.format(df.shape[0]))

    def autoplay(
            self,
            model_weights: str,
            vision: str = 'simple',
            brain_model: str = 'logi',
            output_csv: str = 'moves_auto_play.csv',
            n_move: int = 100,
            n_game: int = 1,
            replay: bool = True,
            replay_fps: int = 5,
            verbose: int = 0) -> None:
        """Predict the best moves that the snake should take to stay alive.
        Args:
            model_weights (str): Path to the weights h5 file.
            brain_model (str): Model to be used as the snake's "brain."
            output_csv (str): Path to save the output csv.
            n_move (int): Number of the moves to be generated.
        """
        if vision == 'simple':
            # 4 simple vision (obstacles) + 4 moves
            n_input = 8
        elif vision == 'advanced':
            # 4 simple vision + 4 advanced visions (apple way) + 4 moves
            n_input = 12
        elif vision == 'expert':
            # 4 simple vision + 4 advanced visions + 4 expert visions (closed regions) + 4 moves
            n_input = 16
        else:
            print('Error: Invalid vision...')
            return

        # build requested brain model
        if brain_model == 'logi':
            self.__brain_model = self.__build_brain_logistic(input_dim=n_input)
        elif brain_model == 'neural_net':
            self.__brain_model = self.__build_brain_neural_net(
                                                        vision=vision,
                                                        input_dim=n_input)
        self.__brain_model.load_weights(model_weights)

        # make `n_move` predictions
        self.simulate(
                n_game=n_game,
                vision_mode=vision,
                n_move=n_move,
                csv=output_csv,
                use_brain=True,
                verbose=(verbose==2))

        # replay predictions
        if replay:
            super().replay(
                        game_id=0,
                        fps=replay_fps,
                        csv=output_csv,
                        ending=False,
                        print_data=(verbose==1 or verbose==2))

    def train(self,
              vision: str = 'simple',
              brain_model: str = 'logi',
              csv: str = 'train.csv',
              epoch: int = 1,
              batch_size: int = 32,
              weights_save_path: str = './brain_models/lr.h5') -> None:
        """Train the snake's brain model.
        Args:
            mdoe (str): "simple", "advanced", "expert"
            brain_model (str): "logi", "neural_net"
        """
        # prep data
        df = pd.read_csv(csv, dtype={
                                'vision': np.object,
                                'vision_simple': np.object,
                                'vision_advanced': np.object,
                                'vision_expert': np.object})
        heads = df.loc[:, 'head_pos']
        apples = df.loc[:, 'apple_pos']
        moves = df.loc[:, 'move']
        results = df.loc[:, 'life']
        facing_apple_series = df.loc[:, 'facing_apple']
        closed_region_series = df.loc[:, 'closed_region']

        # one-hot encoding for visions, targets, and moves
        moves = tf.keras.utils.to_categorical(moves, dtype='int8')
        def str_to_list(str: str) -> list:
            return np.array([int (c) for c in str])
        parser = np.vectorize(str_to_list, signature='()->(n)')
        if vision == 'simple':
            # vision
            visions = parser(df.loc[:, 'vision_simple'])

            # targets
            targets = results
        elif vision == 'advanced':
            # vision
            visions = parser(df.loc[:, 'vision_advanced'])

            # targets
            targets = self.__advanced_vision_targets(results, facing_apple_series)
            targets = tf.keras.utils.to_categorical(targets, dtype='int8')
        elif vision == 'expert':
            # vision
            visions = parser(df.loc[:, 'vision_expert'])

            # targets
            targets = self.__expert_vision_targets(
                                            results,
                                            facing_apple_series,
                                            closed_region_series)
            targets = tf.keras.utils.to_categorical(targets, dtype='int8')
        else:
            # invalid vision; do nothing
            return

        # inputs: [v, v, v, v, ..., m, m, m, m]
        inputs = np.concatenate((visions, moves), axis=1)

        # build model
        if brain_model == 'logi':
            self.__brain_model = self.__build_brain_logistic(
                                            input_dim=inputs.shape[1])
            tf.keras.utils.plot_model(
                            self.__brain_model,
                            to_file='./brain_models/lr_architecture.png')
        elif brain_model == 'neural_net':
            self.__brain_model = self.__build_brain_neural_net(
                                            input_dim=inputs.shape[1],
                                            vision=vision)
            tf.keras.utils.plot_model(
                            self.__brain_model,
                            to_file='./brain_models/nn_architecture.png')
        else:
            # model entered is invalid; do nothing
            return

        # training & save weights
        self.__brain_model.fit(x=inputs,
                               y=targets,
                               shuffle=True,
                               epochs=epoch,
                               batch_size=batch_size,
                               verbose=1)
        self.__brain_model.save_weights(weights_save_path)

    def evaluate(self,
                 test_csv: str,
                 model_weights: str,
                 vision: str = 'simple',
                 brain_model: str = 'logi',
                 sig_thd: float = 0.5) -> None:
        """Test the performance of the brain model using csv data.
        """
        # prep data
        df = pd.read_csv(test_csv, dtype={
                                    'vision': np.object,
                                    'vision_simple': np.object,
                                    'vision_advanced': np.object,
                                    'vision_expert': np.object})
        heads = df.loc[:, 'head_pos']
        apples = df.loc[:, 'apple_pos']
        moves = df.loc[:, 'move']
        results = df.loc[:, 'life']
        facing_apple_series = df.loc[:, 'facing_apple']
        closed_region_series = df.loc[:, 'closed_region']

        # one-hot encoding for visions, targets, and moves
        moves = tf.keras.utils.to_categorical(moves, dtype='int8')
        if vision == 'simple':
            # vision
            visions = df.loc[:, 'vision_simple']
            parser = np.vectorize(super().to_vision_simple, signature='()->(n)')
            visions = parser(visions)

            # targets
            targets = results
        elif vision == 'advanced':
            # vision
            visions = df.loc[:, 'vision_advanced']
            def str_to_list(str: str) -> list:
                return np.array([int (c) for c in str])
            parser = np.vectorize(str_to_list, signature='()->(n)')
            visions = parser(visions)

            # targets
            targets = self.__advanced_vision_targets(results, facing_apple_series)
        elif vision == 'expert':
            # vision
            visions = df.loc[:, 'vision_expert']
            def str_to_list(str: str) -> list:
                return np.array([int (c) for c in str])
            parser = np.vectorize(str_to_list, signature='()->(n)')
            visions = parser(visions)

            # targets
            targets = self.__expert_vision_targets(
                                            results,
                                            facing_apple_series,
                                            closed_region_series)
        else:
            # invalid vision; do nothing
            return

        # inputs: [v, v, v, v, ..., m, m, m, m]
        inputs = np.concatenate((visions, moves), axis=1)

        # build model
        if brain_model == 'logi':
            self.__brain_model = self.__build_brain_logistic(
                                            input_dim=inputs.shape[1])
            tf.keras.utils.plot_model(
                            self.__brain_model,
                            to_file='./brain_models/lr_architecture.png')
        elif brain_model == 'neural_net':
            self.__brain_model = self.__build_brain_neural_net(
                                            input_dim=inputs.shape[1],
                                            vision=vision)
            tf.keras.utils.plot_model(
                            self.__brain_model,
                            to_file='./brain_models/nn_architecture.png')
        else:
            # model entered is invalid; do nothing
            return
        self.__brain_model.load_weights(model_weights)

        if vision == 'simple':
            # predict
            probs = self.__brain_model.predict(inputs).flatten()
            pred_labels = np.zeros(probs.shape[0])
            pred_labels[probs >= sig_thd] = 1

            # print report
            print('')
            print(classification_report(targets, pred_labels))
        elif vision == 'advanced' or vision == 'expert':
            # predict
            probs = self.__brain_model.predict(inputs)
            pred_labels = np.argmax(probs, axis=1)

            # print report
            print('')
            print(classification_report(targets, pred_labels))
        else:
            print('Error: Invalid vision...')

    def __build_brain_neural_net(self,
                                 input_dim: int = 8,
                                 vision: str = 'simple') -> Sequential:
        """A simple neural network with just one single hidden layer; built
        using Keras.
        """
        LEARNING_RATE = 0.001
        DROP_OUT_RATE = 0.5

        model = Sequential()
        if vision == 'simple':
            model.add(InputLayer(input_shape=input_dim))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                          loss='binary_crossentropy')
        elif vision == 'advanced':
            model.add(InputLayer(input_shape=input_dim))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(3, activation='softmax'))
            model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                          loss='categorical_crossentropy')
        elif vision == 'expert':
            model.add(InputLayer(input_shape=input_dim))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(5, activation='softmax'))
            model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                          loss='categorical_crossentropy')
        else:
            print('Error: Invalid vision...')

        return model

    def __build_brain_logistic(self, input_dim: int = 8) -> Sequential:
        """Logistic regression using Keras.
        """
        LEARNING_RATE = 0.001

        model = Sequential()
        model.add(InputLayer(input_shape=input_dim))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                      loss='binary_crossentropy')
        return model

    def __advanced_vision_targets(self,
                                  life_arr: pd.Series,
                                  facing_apple_series: pd.Series,
                                  vision: str = 'simple') -> np.ndarray:
        """Create the targets for examples with advanced vision.
        Returns:
            0 - dead
            1 - survived & apple way
            2 - survived & not apple way
        """
        targets = np.zeros(life_arr.shape[0], dtype=np.uint8)

        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 1)] = 1
        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 0)] = 2

        return targets.reshape((targets.shape[0], 1))

    def __expert_vision_targets(self,
                                life_arr: pd.Series,
                                facing_apple_series: pd.Series,
                                closed_region_arr: pd.Series) -> np.ndarray:
        """Create the targets for examples with advanced vision.
        Returns:
            0 - dead
            1 - survived && apple && !closed
            2 - survived && !apple && !closed
            3 - survived && apple && closed
            4 - survived && !apple && closed
        """
        targets = np.zeros(life_arr.shape[0], dtype=np.uint8)

        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 1) & \
                (closed_region_arr.to_numpy().flatten() == 0)] = 1

        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 0) & \
                (closed_region_arr.to_numpy().flatten() == 0)] = 2

        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 1) & \
                (closed_region_arr.to_numpy().flatten() == 1)] = 3

        targets[(life_arr.to_numpy().flatten() == 1) & \
                (facing_apple_series.to_numpy().flatten() == 0) & \
                (closed_region_arr.to_numpy().flatten() == 1)] = 4

        return targets.reshape((targets.shape[0], 1))

    def __facing_apple(self, move: int, head_pos: tuple, apple_pos: tuple) -> int:
        vision_apple = super().vision_apple(head_pos, apple_pos)
        if (vision_apple[0] == 1 and move == 0) or \
           (vision_apple[1] == 1 and move == 1) or \
           (vision_apple[2] == 1 and move == 2) or \
           (vision_apple[3] == 1 and move == 3):
           return 1
        else:
           return 0
