from Clases_Base.entity import Entity
from Excepciones import InvalidEntityState
from abc import abstractmethod

class Character(Entity):
    """
    Representa un personaje con sistema de vidas
    Atributos adicionales:
    - lives: int - Número de vidas
    - is_alive: bool - Estado de vida
    Métodos:
    - shoot(): abstracto - Crea un disparo
    - collide(): Detecta colisiones
    """
    def __init__(self, x, y, lives=1):
        super().__init__(x, y)
        self._lives = lives
        self._is_alive = True

    @property
    def lives(self): return self._lives
    
    @lives.setter
    def lives(self, value):
        if value < 0: raise InvalidEntityState("Lives cannot be negative")
        self._lives = value
        if value == 0: self._is_alive = False

    @property
    def is_alive(self): return self._is_alive

    @abstractmethod
    def shoot(self): pass

    def collide(self, other): return self.rect.colliderect(other.rect)