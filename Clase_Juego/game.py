import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT
from Clases_Concretas.player import Player
from Clases_Concretas.opponent import Opponent
from Clases_Concretas.boss import Boss


class Game:
    """
    Maneja la lógica principal del juego
    Funcionalidades:
    - Inicialización de Pygame
    - Gestión de eventos y controles
    - Actualización de entidades
    - Detección de colisiones
    - Sistema de puntuación
    - Transición a fase de jefe final
    - Pantallas de game over/victoria
    Métodos clave:
    - start(): Inicia el bucle principal
    - _handle_events(): Gestiona entrada de usuario
    - _update(): Actualiza estado del juego
    - _draw(): Renderiza todos los elementos
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self._is_running = True
        self.score = 0
        self.player = Player(375, 550)
        self.opponents = [Opponent(i*100 + 50, 50) for i in range(5)]
        self.shots = []
        self.boss_active = False

    def start(self):
        while self._is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT: self._is_running = False
            elif event.type == KEYDOWN and event.key == K_SPACE and self.player.is_alive:
                self.shots.append(self.player.shoot())

        keys = pygame.key.get_pressed()
        if self.player.is_alive:
            if keys[K_LEFT]: self.player.move(-5)
            if keys[K_RIGHT]: self.player.move(5)

    def _update(self):
        current_time = pygame.time.get_ticks()
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
                if isinstance(shot, list): self.shots.extend(shot)
                else: self.shots.append(shot)
            if opponent.has_reached_bottom:
                self._end_game(victory=False)
                return

    def _update_shots(self):
        for shot in self.shots[:]:
            shot.move()
            if shot.rect.y < 0 or shot.rect.y > 600: self.shots.remove(shot)

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
                        try: self.shots.remove(shot)
                        except ValueError: pass
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
                if self.player.lives > 0: self.player.respawn()
                else: self._end_game(victory=False)

    def _spawn_boss_if_needed(self):
        if not self.boss_active and not any(isinstance(op, Opponent) for op in self.opponents):
            self.opponents.append(Boss(375, 50))
            self.boss_active = True

    def _draw(self):
        self.screen.fill((0, 0, 0))
        if self.player.is_visible: self.player.draw(self.screen)
        for opponent in self.opponents: opponent.draw(self.screen)
        for shot in self.shots: shot.draw(self.screen)
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render(f'Score: {self.score}', True, (255,255,255)), (10,10))
        self.screen.blit(font.render(f'Lives: {self.player.lives}', True, (255,255,255)), (10,50))
        pygame.display.flip()

    def _end_game(self, victory=False):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render('You Win!' if victory else 'Game Over', True, (0,255,0) if victory else (255,0,0))
        self.screen.blit(text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(3000)
        self._is_running = False
