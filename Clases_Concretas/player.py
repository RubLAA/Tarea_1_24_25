from Clases_Base.character import Character
import pygame
from Clases_Concretas.shot import Shot

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, lives=3)
        # Cargar sprite del jugador
        self.base_image = pygame.image.load('assets/sprites/player_ship.png').convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (50, 50))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Sistema de vidas y cooldown
        self.respawn_time = 0
        self._is_visible = True
        self.last_shot = 0
        self.shot_cooldown = 500
        self.cooldown_progress = 1.0
        self.invulnerable_until = 0  # Tiempo de invulnerabilidad post-respawn

    @property
    def is_visible(self): 
        return self._is_visible

    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if self._is_alive and current_time > self.invulnerable_until:
            self._is_alive = False
            self._is_visible = False
            self.respawn_time = current_time + 2000

    def respawn(self):
        self._is_alive = True
        self._is_visible = True
        self.rect.topleft = (375, 550)
        self.invulnerable_until = pygame.time.get_ticks() + 2000  # 2 seg de invulnerabilidad

    def move(self, dx):
        if self._is_alive:
            self.rect.x += dx
            self.rect.x = max(20, min(self.rect.x, 730))

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

    def draw(self, screen):
        if self._is_visible and self._is_alive:
            current_time = pygame.time.get_ticks()
            
            # Control de opacidad durante invulnerabilidad
            if current_time < self.invulnerable_until:
                # Intercalar opacidad cada 150ms
                alpha = 255 if (current_time // 150) % 2 == 0 else 128
                self.image = self.base_image.copy()
                self.image.set_alpha(alpha)
            else:
                self.image = self.base_image.copy()
                self.image.set_alpha(255)
            
            screen.blit(self.image, self.rect)