import pygame
import random
from Clases_Concretas.opponent import Opponent
from Clases_Concretas.shot import Shot
from Excepciones import InvalidEntityState

class Boss(Opponent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('assets/sprites/boss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(0, 0)
        self._max_health = 20
        self._health = self._max_health
        self._movement_direction = 1  # 1 derecha, -1 izquierda
        self._attack_pattern = 0
        self._special_shot_delay = 3000  # 3 segundos
        self._last_special_shot = 0
        self._base_speed = 2
        self._current_speed = self._base_speed
        self._max_speed = 5
        self._shoot_delay = 1000  # 1 segundo entre disparos
        self._last_shot = 0
        self._phase_two = False
        self._last_radial_attack = 0
        self._radial_cooldown = 3000  # 3 segundos entre ataques


    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        if value < 0:
            raise InvalidEntityState("La salud no puede ser negativa")
        self._health = value

    def move(self):
        # Movimiento principal con control de bordes
        self.rect.x += self._current_speed * self._movement_direction
        
        # Detección precisa de colisión con bordes
        if (self.rect.left < 0 and self._movement_direction == -1) or \
           (self.rect.right > 800 and self._movement_direction == 1):
            
            # Ajustar posición al borde
            if self._movement_direction == -1:
                self.rect.left = 0
            else:
                self.rect.right = 800
            
            self._movement_direction *= -1
            self._change_attack_pattern()
            
            # Pequeño ajuste para evitar rebote infinito
            self.rect.x += self._movement_direction * 2

        self.hitbox.center = self.rect.center

    def _change_attack_pattern(self):
        self._attack_pattern = random.choice([0, 1, 2])
        self._current_speed = max(self._base_speed, 1)  # Velocidad mínima

    def shoot(self):
        current_time = pygame.time.get_ticks()
        shots = []
        
        # Entrar en fase 2 al 50% de vida
        if not self._phase_two and self._health <= self._max_health // 2:
            self._phase_two = True

        # Ataque radial periódico en fase 2
        if self._phase_two:
            if current_time - self._last_radial_attack > self._radial_cooldown:
                shots += self._radial_attack()
                self._last_radial_attack = current_time
        
        # Ataques normales (se mantienen)
        if current_time - self._last_shot > self._shoot_delay:
            self._last_shot = current_time
        
        # Ataque especial cada 3 segundos
        if current_time - self._last_special_shot > self._special_shot_delay:
            self._last_special_shot = current_time
            return self._special_attack()
        
        # Ataques normales
        if current_time - self._last_shot > self._shoot_delay:
            self._last_shot = current_time
            
            if self._attack_pattern == 0:
                # Disparo frontal
                shots.append(Shot(self.rect.centerx, self.rect.bottom, 'down', 'boss', (255, 0, 255)))
            elif self._attack_pattern == 1:
                # Doble disparo lateral
                shots.extend([
                    Shot(self.rect.left + 10, self.rect.bottom, 'down', 'boss'),
                    Shot(self.rect.right - 10, self.rect.bottom, 'down', 'boss')
                ])
            else:
                # Aumento de velocidad controlado
                self._current_speed = min(self._current_speed * 1.2, self._max_speed)
        
        return shots
    
    def _radial_attack(self):
        projectiles = []
        # 16 disparos en círculo con ángulos aleatorios
        for _ in range(16):
            angle = random.uniform(0, 360)
            projectile = Shot(self.rect.centerx, self.rect.centery, 'down', 'boss', (255, 0, 0))
            projectile._offset_angle(angle)
            projectiles.append(projectile)
        
        return projectiles

    def _special_attack(self):
        # Triple disparo angular
        return [
            Shot(self.rect.centerx, self.rect.bottom, 'down', 'boss', (255, 0, 255)),
            Shot(self.rect.centerx - 30, self.rect.bottom, 'down', 'boss', (255, 0, 255))._offset_angle(-15),
            Shot(self.rect.centerx + 30, self.rect.bottom, 'down', 'boss', (255, 0, 255))._offset_angle(15)
        ]

    def draw(self, screen):
        # Dibujar sprite
        screen.blit(self.image, self.rect)
                
        # Dibujar barra de salud
        bar_width = self.rect.width
        bar_height = 7
        health_width = (self._health / self._max_health) * bar_width
        
        pygame.draw.rect(screen, (255, 0, 0),   # Fondo rojo
                        (self.rect.x, self.rect.y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0),   # Barra verde de salud
                        (self.rect.x, self.rect.y - 15, health_width, bar_height))