from abc import ABC, abstractmethod
import pygame

class Entity(ABC):
    """
    Representa una entidad básica del juego
    Atributos:
    - rect: pygame.Rect - Posición y dimensiones
    - color: tuple - Color RGB
    Métodos:
    - move(): abstracto - Define el movimiento
    - draw(): Dibuja la entidad en pantalla
    """
    def __init__(self, x, y, width=50, height=50, color=(255, 0, 0)):
        self._rect = pygame.Rect(x, y, width, height)
        self._color = color
    
    @property
    def rect(self): return self._rect
    
    @rect.setter
    def rect(self, value):
        if not isinstance(value, pygame.Rect):
            raise ValueError("rect must be a pygame.Rect")
        self._rect = value
    
    @property
    def color(self): return self._color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, tuple) or len(value) != 3:
            raise ValueError("Color must be a tuple of 3 integers")
        self._color = value

    @abstractmethod
    def move(self): pass

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self._rect)