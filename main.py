from Clase_Juego.game import Game
from Excepciones import GameException
import pygame

if __name__ == "__main__":
    try: Game().start()
    except GameException as e: print(f"Game Error: {e}")
    except Exception as e: print(f"Unexpected Error: {e}")
    finally: pygame.quit()