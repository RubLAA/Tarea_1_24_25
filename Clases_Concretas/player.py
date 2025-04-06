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
        self.last_shot = 0  # Tiempo del último disparo
        self.shot_cooldown = 500  # Cooldown en milisegundos (0.5 segundos)
        self.cooldown_progress = 1.0

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

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shot_cooldown:
            self.last_shot = current_time
            self.cooldown_progress = 0.0
            return Shot(self.rect.centerx, self.rect.top, 'up', 'player')
        return None
    
    def update_cooldown(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_shot
        self.cooldown_progress = min(elapsed / self.shot_cooldown, 1.0)