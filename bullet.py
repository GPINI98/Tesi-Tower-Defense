# bullet.py
import pygame
import config
from pygame.math import Vector2

class Bullet:
    def __init__(self, x, y, target, damage, level=1):
        self.pos = Vector2(x, y)
        self.target = target
        self.damage = damage
        self.level = level
        
        # Caratteristiche del proiettile scalate in base al livello della torre
        if self.level == 1:
            self.speed = config.BULLET_SPEED
            self.radius = 5
            self.color = config.YELLOW
        elif self.level == 2:
            self.speed = config.BULLET_SPEED + 2      # Più veloce
            self.radius = 7                           # Più grande
            self.color = (255, 140, 0)                # Arancione brillante
        else: # Livello 3 e successivi
            self.speed = config.BULLET_SPEED + 4      # Molto veloce
            self.radius = 9                           # Grande
            self.color = (0, 255, 255)                # Ciano energetico

    def update(self, enemies_list):
        """
        Aggiorna la posizione del proiettile verso il bersaglio.
        Ritorna True se ha colpito o se il bersaglio non esiste più.
        """
        if self.target not in enemies_list or self.target.health <= 0:
            return True

        target_pos = Vector2(self.target.rect.centerx, self.target.rect.centery)
        direzione = target_pos - self.pos
        distanza = direzione.length()

        if distanza <= self.speed:
            self.target.health -= self.damage
            return True
        else:
            direzione_normalizzata = direzione.normalize()
            self.pos += direzione_normalizzata * self.speed
            return False

    def draw(self, screen):
        """Disegna il proiettile a schermo."""
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)