from Clases_Base.character import Character
import pygame
from Clases_Concretas.shot import Shot

class Player(Character):
    """
    Controla al jugador principal
    Características:
    - 3 vidas iniciales
    - Movimiento lateral
    - Sistema de respawn con invulnerabilidad temporal
    - Disparos verticales hacia arriba
    Métodos principales:
    - move(): Control por teclado
    - shoot(): Crea disparos del jugador
    - take_damage(): Maneja el daño recibido
    """
    def __init__(self, x, y):
        super().__init__(x, y, lives=3)
        self._color = (0, 0, 255)
        self.respawn_time = 0
        self._is_visible = True

    @property
    def is_visible(self): return self._is_visible

    def take_damage(self):
        if self._is_alive:
            self._is_alive = False
            self._is_visible = False
            self.respawn_time = pygame.time.get_ticks() + 2000

    def respawn(self):
        self._is_alive = True
        self._is_visible = True
        self.rect.topleft = (375, 550)

    def move(self, dx):
        if self._is_alive:
            self.rect.x += dx
            self.rect.x = max(0, min(self.rect.x, 750))

    def shoot(self): return Shot(self.rect.centerx, self.rect.top, 'up', 'player')