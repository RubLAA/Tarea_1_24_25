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
        self.wave = 1
        self.enemies_per_wave = 5  # Enemigos iniciales por oleada
        self.time_since_last_wave = 0
        self.wave_delay = 5000
        self.round_count = 0
        self.wave = 1
        self.wave_completed = False
        self._spawn_wave()  # Generar primera oleada

    def _spawn_wave(self):
        """Genera una nueva oleada de enemigos."""
        if not self.opponents:  # Solo generar nueva oleada si no hay enemigos activos
            num_enemies = self.enemies_per_wave
            spacing = 800 / (num_enemies + 1)
            for i in range(num_enemies):
                x = spacing * (i + 1)
                self.opponents.append(Opponent(x, 50))
            
            self.wave_completed = False  # Resetear la bandera al generar nueva oleada
            self.wave += 1  # Incrementar el contador de oleadas

    def _spawn_boss_if_needed(self):
        """Verifica si se debe generar el jefe al finalizar una oleada."""
        # Corregir condición para excluir Boss
        if not self.boss_active and not any(
            (isinstance(op, Opponent) and not isinstance(op, Boss)) 
            for op in self.opponents
        ):
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
        
        # Verificar si la oleada actual está completada (no hay enemigos)
        if not self.opponents and not self.wave_completed:
            self.wave_completed = True
            # Reducir el número de oleada si es mayor que 1
            if self.wave > 1:
                self.wave -= 1
            
            # Esperar un tiempo antes de generar nueva oleada
            self.time_since_last_wave = current_time
        
        # Generar nueva oleada después del delay
        if self.wave_completed and current_time - self.time_since_last_wave > self.wave_delay:
            self._spawn_wave()
        
        # Resto de la lógica de actualización...
        self._update_opponents()
        self._update_shots()
        self._check_collisions()
        self._handle_respawn(current_time)
        self._spawn_boss_if_needed()
    
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
                if not any(isinstance(e, Boss) for e in self.opponents):
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