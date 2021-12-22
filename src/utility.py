import pygame.font as pygame_font


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DevelopmentMode(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    def on(self) -> bool:
        return False

    def off(self) -> bool:
        return not self.on()


class SharedFont(metaclass=SingletonMeta):
    FONT_PATH = "fonts/ClearSans-Bold.ttf"

    def __init__(self) -> None:
        self.fonts = dict()

    def get_font(self, size) -> pygame_font.Font:
        if self.fonts.get(size) is None:
            self.fonts[size] = pygame_font.Font(self.FONT_PATH, size)

        return self.fonts[size]
