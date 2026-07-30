# bullet.py
import pygame
import config
from pygame.math import Vector2

class Bullet:
    def __init__(self, x, y, target, damage):
        self.pos = Vector2(x, y)
        self.target = target
        self.damage = damage
        self.speed = config.BULLET_SPEED
        self.radius = config.BULLET_SIZE
        self.color = config.YELLOW

    def update(self, enemies_list):
        """
        Aggiorna la posizione del proiettile verso il bersaglio.
        Ritorna True se il proiettile ha colpito il bersaglio o se il bersaglio non esiste più.
        """
        # Se il nemico è stato già eliminato o rimosso dalla lista
        if self.target not in enemies_list or self.target.health <= 0:
            return True # Segnale di rimozione

        # Coordinate attuali del centro del nemico bersaglio
        target_pos = Vector2(self.target.rect.centerx, self.target.rect.centery)
        
        # Vettore direzione e distanza
        direzione = target_pos - self.pos
        distanza = direzione.length()

        # Controllo collisione (se la distanza è inferiore allo spostamento in un frame)
        if distanza <= self.speed:
            self.target.health -= self.damage # Applica il danno al nemico
            return True # Segnale di rimozione (colpo andato a segno)
        else:
            # Movimento vettoriale normalizzato verso il target
            direzione_normalizzata = direzione.normalize()
            self.pos += direzione_normalizzata * self.speed
            return False # Il proiettile continua a viaggiare

    def draw(self, screen):
        """Disegna il proiettile a schermo."""
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)