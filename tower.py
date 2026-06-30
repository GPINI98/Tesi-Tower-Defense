# tower.py
import pygame
import math
import config

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = config.BLUE
        self.range = config.TOWER_RANGE

    def draw(self, screen, enemy=None):
        # Calcoliamo il centro della torre
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        # 1. Disegna il raggio d'azione
        pygame.draw.circle(screen, config.WHITE, (center_x, center_y), self.range, 1)

        # 2. Disegna la torre
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

        # 3. Logica di "Puntamento" (Radar)
        if enemy:
            # Calcoliamo il centro del nemico
            enemy_center_x = enemy.x + enemy.width // 2
            enemy_center_y = enemy.y + enemy.height // 2
            
            # Calcolo della distanza (Distanza Euclidea)
            distanza = math.hypot(enemy_center_x - center_x, enemy_center_y - center_y)
            
            # Se il nemico è dentro il cerchio, spara un laser!
            if distanza <= self.range:
                pygame.draw.line(screen, config.RED, (center_x, center_y), (enemy_center_x, enemy_center_y), 3)