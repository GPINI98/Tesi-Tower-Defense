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
        self.level = 1
        self.range = config.TOWER_RANGE
        self.damage = 1
        self.upgrade_cost = config.UPGRADE_COST
        
        # Creiamo un Rect standard di Pygame per gestire la geometria della torre
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
    
    def upgrade(self):
        """Potenzia la torre aumentando raggio e danno"""
        self.level += 1
        self.range += 20     # Aumenta il raggio
        self.damage += 0.5   # Aumenta il danno per frame
        self.upgrade_cost = int(self.upgrade_cost * 1.5) # Il prossimo upgrade costerà di più
        
        # Cambia leggermente colore per far capire che è potenziata
        if self.level == 2:
            self.color = (0, 150, 255) # Azzurro
        elif self.level >= 3:
            self.color = (0, 255, 255) # Ciano
    
    def draw(self, screen, enemies):
        # Calcoliamo il centro geometrico della torre usando il rect
        center_x = self.rect.centerx
        center_y = self.rect.centery

        # 1. Disegna il raggio d'azione
        pygame.draw.circle(screen, config.WHITE, (center_x, center_y), self.range, 1)

        # 2. Disegna la torre
        pygame.draw.rect(screen, self.color, self.rect)

        # Mostra il livello della torre al centro
        font = pygame.font.SysFont(None, 24)
        lvl_text = font.render(str(self.level), True, config.WHITE)
        screen.blit(lvl_text, (self.rect.x + 15, self.rect.y + 10))

   # Logica di Puntamento: cerca nella lista dei nemici
        for enemy in enemies:
            if enemy.health > 0:
                enemy_cx = enemy.rect.centerx
                enemy_cy = enemy.rect.centery
                distanza = math.hypot(enemy_cx - center_x, enemy_cy - center_y)
                
                # Se è nel raggio, spara e FERMATI (spara a un solo nemico alla volta)
                if distanza <= self.range:
                    pygame.draw.line(screen, config.RED, (center_x, center_y), (enemy_cx, enemy_cy), 3)
                    enemy.health -= self.damage
                    break