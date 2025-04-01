import pygame
import random
from Clases_Concretas.opponent import Opponent
from Clases_Concretas.shot import Shot
from Excepciones import InvalidEntityState



class Boss(Opponent):
    """
    Jefe final con características especiales:
    - Mayor tamaño y salud (20 puntos)
    - Movimiento horizontal alternante
    - Múltiples patrones de ataque
    - Barra de salud visible
    - Ataques especiales con disparos angulados
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 80, 80)
        self._color = (255, 165, 0)
        self._max_health = 20
        self._health = self._max_health
        self._movement_direction = 1
        self._attack_pattern = 0
        self._special_shot_delay = 3000
        self._last_special_shot = 0

    @property
    def health(self): return self._health
    
    @health.setter
    def health(self, value):
        if value < 0: raise InvalidEntityState("Health cannot be negative")
        self._health = value

    def move(self):
        self.rect.x += self._speed * self._movement_direction
        if self.rect.left <= 0 or self.rect.right >= 800:
            self._movement_direction *= -1
            self._change_attack_pattern()

    def _change_attack_pattern(self):
        self._attack_pattern = random.choice([0, 1, 2])

    def shoot(self):
        shots = []
        current_time = pygame.time.get_ticks()
        
        if current_time - self._last_special_shot > self._special_shot_delay:
            self._last_special_shot = current_time
            return self._special_attack()
            
        if current_time - self._last_shot > self._shoot_delay:
            self._last_shot = current_time
            if self._attack_pattern == 0:
                shots.append(Shot(self.rect.centerx, self.rect.bottom, 'down', 'boss', (255, 0, 255)))
            elif self._attack_pattern == 1:
                shots.extend([
                    Shot(self.rect.left, self.rect.bottom, 'down', 'boss'),
                    Shot(self.rect.right, self.rect.bottom, 'down', 'boss')
                ])
            else: self._speed *= 1.5
        return shots

    def _special_attack(self):
        return [
            Shot(self.rect.centerx, self.rect.bottom, 'down', 'boss', (255, 0, 255)),
            Shot(self.rect.centerx - 20, self.rect.bottom, 'down', 'boss', (255, 0, 255))._offset_angle(-10),
            Shot(self.rect.centerx + 20, self.rect.bottom, 'down', 'boss', (255, 0, 255))._offset_angle(10)
        ]

    def draw(self, screen):
        super().draw(screen)
        bar_width = self.rect.width
        bar_height = 7
        fill = (self._health / self._max_health) * bar_width
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 15, fill, bar_height))