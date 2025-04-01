from Clases_Base.entity import Entity
import math

class Shot(Entity):
    """
    Representa un disparo en el juego
    Características:
    - Dirección (arriba/abajo)
    - Dueño (jugador/enemigo)
    - Posibilidad de movimiento angular
    - Auto-destrucción al salir de pantalla
    """
    def __init__(self, x, y, direction, owner, color=(0, 255, 0)):
        super().__init__(x, y, 5, 10, color)
        self._direction = direction
        self._owner = owner
        self._base_speed = 5
        self._angle = 0
    
    def _offset_angle(self, degrees):
        self._angle = degrees
        return self
        
    def move(self):
        if self._direction == 'up': self._rect.y -= self._base_speed
        else: self._rect.y += self._base_speed
        self._rect.x += math.sin(math.radians(self._angle)) * 3