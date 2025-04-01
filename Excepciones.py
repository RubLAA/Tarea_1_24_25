class GameException(Exception): 
    """Excepción base para errores del juego"""
    pass
class InvalidEntityState(GameException): 
    """Se lanza cuando una entidad tiene un estado inválido"""
    pass