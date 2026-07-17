# tower.py
import pygame
import math
import config

class Tower:
    def __init__(self, x, y):
        # Definiamo la posizione e le dimensioni
        self.width = 40
        self.height = 40
        self.color = config.BLUE
        self.range = config.TOWER_RANGE
        
        # Creiamo un Rect standard di Pygame per gestire la geometria della torre
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen, enemy=None):
        # Calcoliamo il centro geometrico della torre usando il rect
        center_x = self.rect.centerx
        center_y = self.rect.centery

        # 1. Disegna il raggio d'azione
        pygame.draw.circle(screen, config.WHITE, (center_x, center_y), self.range, 1)

        # 2. Disegna la torre
        pygame.draw.rect(screen, self.color, self.rect)

        # Radar
        if enemy:
            # Calcoliamo il centro del nemico sfruttando il suo rect
            enemy_center_x = enemy.rect.centerx
            enemy_center_y = enemy.rect.centery
            
            # Calcolo della distanza (Distanza Euclidea)
            distanza = math.hypot(enemy_center_x - center_x, enemy_center_y - center_y)
            
            # Se il nemico è nel raggio d'azione, disegna la linea laser e infliggi danno
            if distanza <= self.range:
                pygame.draw.line(screen, config.RED, (center_x, center_y), (enemy_center_x, enemy_center_y), 3)
                enemy.health -= 1  # La torre infligge danno progressivo