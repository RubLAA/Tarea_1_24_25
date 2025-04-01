from Clases_Base.character import Character
import pygame
import math
from Clases_Concretas.shot import Shot

class Opponent(Character):
    """
    Enemigo básico
    Características:
    - Movimiento sinusoidal hacia abajo
    - Disparos automáticos cada 2 segundos
    - Al llegar al fondo termina el juego
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self._base_color = (255, 0, 0)
        self._color = self._base_color
        self._speed = 1.2
        self._shoot_delay = 2000
        self._last_shot = pygame.time.get_ticks()
        self._has_reached_bottom = False

    def move(self):
        self._rect.y += self._speed
        self._rect.x += 2 * math.sin(pygame.time.get_ticks()/200)
        if self._rect.bottom >= 600: self._has_reached_bottom = True

    @property
    def has_reached_bottom(self): return self._has_reached_bottom
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self._last_shot > self._shoot_delay:
            self._last_shot = current_time
            return Shot(self.rect.centerx, self.rect.bottom, 'down', 'opponent')
        return None