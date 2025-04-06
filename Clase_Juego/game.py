import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT
from Clases_Concretas.player import Player
from Clases_Concretas.opponent import Opponent
from Clases_Concretas.boss import Boss

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self._is_running = True
        self.score = 0
        self.player = Player(375, 550)
        self.opponents = []
        self.shots = []
        self.boss_active = False
        self.wave = 5  # Oleadas iniciales antes del jefe
        self.enemies_per_wave = 5
        self.time_since_last_wave = 0
        self.wave_delay = 5000
        self.wave = 5  # Oleadas iniciales antes del jefe
        self.formation_pattern = 0  # Patrón de formación actual
        self._spawn_wave()

    def _spawn_wave(self):
        """Genera enemigos en diferentes formaciones por oleada"""
        num_enemies = self.enemies_per_wave
        formation = self.wave % 3  # Rotar entre 3 formaciones
        
        if formation == 0:  # Formación escalonada
            self._create_staggered_formation(num_enemies)
        elif formation == 1:  # Formación diamante
            self._create_diamond_formation(num_enemies)
        else:  # Formación doble fila
            self._create_double_row_formation(num_enemies)
        
        self.enemies_per_wave += 2

    def _create_staggered_formation(self, num_enemies):
        """Formación con filas desplazadas alternadamente"""
        rows = 2 + (self.wave // 3)
        vertical_spacing = 50
        enemies_per_row = num_enemies // rows
        
        for row in range(rows):
            y = 50 + row * vertical_spacing
            x_offset = 40 if row % 2 == 0 else 0  # Desplazamiento alterno
            spacing = (800 - x_offset) / (enemies_per_row + 1)
            
            for i in range(enemies_per_row + (1 if row < num_enemies % rows else 0)):
                x = x_offset + spacing * (i + 1)
                self.opponents.append(Opponent(x, y))

    def _create_diamond_formation(self, num_enemies):
        """Formación en diamante centrado"""
        center_x, center_y = 400, 100
        max_layers = 3
        enemies_added = 0
        
        for layer in range(max_layers):
            layer_enemies = 1 + 2 * layer
            spacing = 600 // (layer + 1)
            
            for i in range(layer_enemies):
                x = center_x + (i - layer) * spacing
                y = center_y + layer * 50
                if 0 < x < 800 and enemies_added < num_enemies:
                    self.opponents.append(Opponent(x, y))
                    enemies_added += 1
            
            if enemies_added >= num_enemies:
                break

    def _create_double_row_formation(self, num_enemies):
        """Dos filas con diferentes espaciados"""
        row1_enemies = num_enemies // 2
        row2_enemies = num_enemies - row1_enemies
        
        # Primera fila
        spacing = 800 / (row1_enemies + 1)
        for i in range(row1_enemies):
            self.opponents.append(Opponent(spacing * (i + 1), 50))
        
        # Segunda fila
        spacing = 800 / (row2_enemies + 1)
        for i in range(row2_enemies):
            self.opponents.append(Opponent(spacing * (i + 1), 120))

    def _spawn_boss(self):
        """Genera el jefe final"""
        if not self.boss_active:
            self.opponents.append(Boss(375, 50))
            self.boss_active = True

    def start(self):
        while self._is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._is_running = False
            elif event.type == KEYDOWN and event.key == K_SPACE and self.player.is_alive:
                self.shots.append(self.player.shoot())
        keys = pygame.key.get_pressed()
        if self.player.is_alive:
            if keys[K_LEFT]:
                self.player.move(-5)
            if keys[K_RIGHT]:
                self.player.move(5)
    
    def _update(self):
        current_time = pygame.time.get_ticks()
        
        # Verificar si se completó una oleada
        if not self.opponents and not self.boss_active:
            if self.wave > 0:
                self.wave -= 1  # Reducir contador de oleadas
                self._spawn_wave()
            else:
                self._spawn_boss()

        self._update_opponents()
        self._update_shots()
        self._check_collisions()
        self._handle_respawn(current_time)
    
    def _update_opponents(self):
        for opponent in self.opponents[:]:
            opponent.move()
            shot = opponent.shoot()
            if shot:
                if isinstance(shot, list):
                    self.shots.extend(shot)
                else:
                    self.shots.append(shot)
            if opponent.has_reached_bottom:
                self._end_game(victory=False)
                return
    
    def _update_shots(self):
        for shot in self.shots[:]:
            shot.move()
            if shot.rect.y < 0 or shot.rect.y > 600:
                self.shots.remove(shot)
    
    def _check_collisions(self):
        for shot in self.shots[:]:
            if shot._owner in ['opponent', 'boss'] and self.player.collide(shot):
                self._handle_player_hit()
                self.shots.remove(shot)
                break
        for shot in self.shots[:]:
            if shot._owner == 'player':
                for opponent in self.opponents[:]:
                    if opponent.collide(shot):
                        self._handle_enemy_hit(opponent)
                        self.shots.remove(shot)
                        break
    
    def _handle_enemy_hit(self, enemy):
        if isinstance(enemy, Boss):
            enemy.health -= 1
            if enemy.health <= 0:
                self.opponents.remove(enemy)
                self.score += 15
                self.boss_active = False
                self._end_game(victory=True)
        else:
            self.opponents.remove(enemy)
            self.score += 1
    
    def _handle_player_hit(self):
        if self.player.is_alive:
            self.player.lives -= 1
            self.player._is_alive = False
            self.player._is_visible = False
            self.player.respawn_time = pygame.time.get_ticks() + 2000
            self.screen.fill((255, 0, 0))
            pygame.display.flip()
            pygame.time.delay(100)
    
    def _handle_respawn(self, current_time):
        if not self.player.is_alive:
            self.player._is_visible = (current_time // 250) % 2 == 0
            if current_time > self.player.respawn_time:
                if self.player.lives > 0:
                    self.player.respawn()
                else:
                    self._end_game(victory=False)

    def _spawn_opponents(self):
        """
        Genera enemigos en rondas con un aumento en su número.
        """
        self.time_since_last_wave = pygame.time.get_ticks()
        # Aumentar el número de enemigos en cada ronda
        for i in range(self.round_count * 2):  # Aumentamos 2 enemigos por ronda
            # Ajustamos el rango para que los enemigos no se superpongan en el inicio
            x_position = (i % 5) * 100 + 50
            y_position = 50
            self.opponents.append(Opponent(x_position, y_position))

        # Incrementamos el contador de rondas
        self.round_count += 1
    
    def _spawn_boss_if_needed(self):
        if not self.boss_active and self.wave % 5 == 0:
            self.opponents.append(Boss(375, 50))
            self.boss_active = True
    
    def _draw(self):
        self.screen.fill((0, 0, 0))
        if self.player.is_visible:
            self.player.draw(self.screen)
        for opponent in self.opponents:
            opponent.draw(self.screen)
        for shot in self.shots:
            shot.draw(self.screen)
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render(f'Score: {self.score}', True, (255,255,255)), (10,10))
        self.screen.blit(font.render(f'Lives: {self.player.lives}', True, (255,255,255)), (10,50))
        self.screen.blit(font.render(f'Wave: {self.wave}', True, (255,255,255)), (10,90))
        pygame.display.flip()
    
    def _end_game(self, victory=False):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('You Win!' if victory else 'Game Over', True, (0,255,0) if victory else (255,0,0))
        self.screen.blit(text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(3000)
        self._is_running = False