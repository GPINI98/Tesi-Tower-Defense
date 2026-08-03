# tower.py
import pygame
import math
import config
from bullet import Bullet

class Tower:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.color = config.BLUE
        self.level = 1
        self.range = config.TOWER_RANGE
        self.damage = 25     # Danno inflitto da ogni proiettile
        self.upgrade_cost = config.UPGRADE_COST
        
        # Rettangolo di collisione / posizionamento
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        
        # Gestione Cadenza di Tiro (Cooldown basato sui frame o timer)
        self.cooldown_max = 45 # Numero di frame di attesa tra un colpo e l'altro
        self.cooldown_timer = 0
    
    def upgrade(self):
        """Potenzia la torre aumentando raggio e danno"""
        self.level += 1
        self.range += 20     # Aumenta il raggio
        self.damage += 15    # Aumenta il danno
        self.upgrade_cost = int(self.upgrade_cost * 1.5)
        
        if self.level == 2:
            self.color = (0, 150, 255) # Azzurro
        elif self.level >= 3:
            self.color = (0, 255, 255) # Ciano
    
    def update(self, enemies, bullets_list):
        """Gestisce il decremento del timer di sparo e la ricerca geometrica del bersaglio"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        center_x = self.rect.centerx
        center_y = self.rect.centery

        # Algoritmo di Puntamento Geometrico (Distanza Euclidea minima)
        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            if enemy.health > 0:
                enemy_cx = enemy.rect.centerx
                enemy_cy = enemy.rect.centery
                distanza = math.hypot(enemy_cx - center_x, enemy_cy - center_y)
                
                # Se il nemico è nel raggio d'azione ed è il più vicino 
                if distanza <= self.range and distanza < min_distance:
                    min_distance = distanza
                    closest_enemy = enemy

        # Se troviamo un bersaglio valido e la torre ha ricaricato, spara (crea proiettile)
        # Se troviamo un bersaglio valido e la torre ha ricaricato, spara
        if closest_enemy and self.cooldown_timer == 0:
            # Passiamo self.level al proiettile
            new_bullet = Bullet(center_x, center_y, closest_enemy, self.damage, self.level)
            bullets_list.append(new_bullet)
            self.cooldown_timer = self.cooldown_max

    def draw(self, screen):
        """Disegna unicamente gli elementi grafici della torretta"""
        center_x = self.rect.centerx
        center_y = self.rect.centery

        # 1. Disegna il raggio d'azione (cerchio trasparente o sottile)
        pygame.draw.circle(screen, config.WHITE, (center_x, center_y), self.range, 1)

        # 2. Disegna la torre
        pygame.draw.rect(screen, self.color, self.rect)

        # 3. Mostra il livello della torre al centro
        font = pygame.font.SysFont(None, 24)
        lvl_text = font.render(str(self.level), True, config.WHITE)
        screen.blit(lvl_text, (self.rect.x + 12, self.rect.y + 10))