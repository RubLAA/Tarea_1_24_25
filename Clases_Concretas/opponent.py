from Clases_Base.character import Character
import pygame
from Clases_Concretas.shot import Shot

class Opponent(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('assets/sprites/enemy_basic.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._base_color = (255, 0, 0)
        self._color = self._base_color
        self._speed = 1.2
        self._shoot_delay = 2000
        self._last_shot = pygame.time.get_ticks()
        self._has_reached_bottom = False
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 1
        self.target_y = y
        self.entering = True
        self.max_y = 400  # Límite máximo inferior para el movimiento
        self.hitbox = self.rect.inflate( -5, -5)  # Reduce 6px por lado

    def move(self):
        if self.entering:
            # Movimiento controlado de entrada
            if self.rect.y < self.target_y:
                self.rect.y += self.speed * 2
            else:
                self.entering = False
        else:
            # Movimiento lateral con límite inferior
            self.rect.x += self.speed
            
            # Limitar movimiento horizontal a la pantalla
            if self.rect.right > 780 or self.rect.left < 20:
                self.speed *= -1
                # Descenso controlado sin sobrepasar el límite
                if self.rect.y < self.max_y:
                    self.rect.y += 20
                else:
                    # Si ya está en el límite, solo cambia dirección
                    self.speed *= -1
            
            # Limitar posición vertical
            self.rect.y = min(self.rect.y, self.max_y)
        self.hitbox.center = self.rect.center

    @property
    def has_reached_bottom(self): return self._has_reached_bottom
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self._last_shot > self._shoot_delay:
            self._last_shot = current_time
            return Shot(self.rect.centerx, self.rect.bottom, 'down', 'opponent')
        return None
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)