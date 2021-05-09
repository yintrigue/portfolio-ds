import pygame

class SpriteSheet:
    """SpriteSheet provides basic properties and methods for process a sprite
    sheet for pygame.
    """
    def __init__(self, filename: str):
        self.__filename = filename
        self.__sheet = None # pygame.Surface

    def load(self) -> None:
        try:
            self.__sheet = pygame.image.load(self.__filename).convert_alpha()
        except:
            print('404: Unable to load spritesheet image...')
            raise

    def image_at(self, rectangle: tuple) -> None:
        """
        Args:
            rectangle (tuple): *x, y, x_offset, y_offset)
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.__sheet, (0, 0), rect)

        return image

class SnakeSprite(SpriteSheet):
    """Sprite for the pygame, Snaky.
    """
    def __init__(self, snake_file: str, apple_file: str, dim: int):
        super().__init__(snake_file)

        self.__dim = dim
        self.__head = [] # 0: u, 1: r, 2: d, 3: l
        self.__body = []
        self.__body_turn = []
        self.__tail = []

        self.__apple_file = apple_file
        self.__apple = None

    def load(self) -> None:
        # load apple
        self.__apple = pygame.image.load(self.__apple_file).convert_alpha()
        self.__apple = pygame.transform.scale(self.__apple, (self.__dim, self.__dim))

        # load snake
        super().load()

        head = super().image_at((0, 0, 200, 200))
        head = pygame.transform.scale(head, (self.__dim, self.__dim))
        self.__head = (
            pygame.transform.rotate(head, 0),
            pygame.transform.rotate(head, -90),
            pygame.transform.rotate(head, -180),
            pygame.transform.rotate(head, -270))

        body = super().image_at((0, 400, 200, 200))
        body = pygame.transform.scale(body, (self.__dim, self.__dim))
        self.__body = (
            pygame.transform.rotate(body, 0),
            pygame.transform.rotate(body, -90),
            pygame.transform.rotate(body, -180),
            pygame.transform.rotate(body, -270))

        body_turn = super().image_at((0, 200, 200, 200))
        body_turn = pygame.transform.scale(body_turn, (self.__dim, self.__dim))
        body_turn_cw = (
            pygame.transform.rotate(body_turn, 0),
            pygame.transform.rotate(body_turn, -90),
            pygame.transform.rotate(body_turn, -180),
            pygame.transform.rotate(body_turn, -270))

        body_turn = pygame.transform.flip(body_turn, True, False)
        body_turn_ccw = (
            pygame.transform.rotate(body_turn, 0),
            pygame.transform.rotate(body_turn, -90),
            pygame.transform.rotate(body_turn, -180),
            pygame.transform.rotate(body_turn, -270))
        self.__body_turn = body_turn_cw + body_turn_ccw

        tail = super().image_at((0, 600, 200, 200))
        tail = pygame.transform.scale(tail, (self.__dim, self.__dim))
        self.__tail = (pygame.transform.rotate(tail, 0),
                       pygame.transform.rotate(tail, -90),
                       pygame.transform.rotate(tail, -180),
                       pygame.transform.rotate(tail, -270))

    @property
    def apple(self) -> pygame.Surface:
        return self.__apple

    @property
    def head(self) -> list:
        return self.__head

    @property
    def body(self) -> list:
        return self.__body

    @property
    def body_turn(self) -> list:
        return self.__body_turn

    @property
    def tail(self) -> list:
        return self.__tail
